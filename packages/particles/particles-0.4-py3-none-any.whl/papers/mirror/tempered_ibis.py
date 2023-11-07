import numpy as np
from scipy import optimize

from particles import resampling as rs
from particles import smc_samplers as ssps

class TemperedIBIS(ssps.FKSMCsampler):
    def __init__(self, model=None, wastefree=True, len_chain=10, move=None,
                 batch=1, ESSrmin=0.5):
        super().__init__(model=model, wastefree=wastefree, len_chain=len_chain,
                         move=move)
        self.batch = batch
        self.ESSrmin = ESSrmin
        r, m = divmod(self.T, self.batch)
        self.maxbatch = r + 1 if m > 0 else r

    def summary_format(self, smc):
        msg = super().summary_format(smc)
        b = smc.X.shared['batch']
        epn = smc.X.shared['epn']
        return f'{msg}, batch={b}, tempering exponent={epn}'

    def time_to_resample(self, smc):
        ESSmin = self.ESSrmin * smc.X.N
        rs_flag = (smc.X.shared['epn'] < 1.) or (smc.aux.ESS < ESSmin)
        smc.X.shared['rs_flag'] = rs_flag
        if rs_flag:
            self.move.calibrate(smc.W, smc.X)
        return rs_flag

    def done(self, smc):
        if smc.X is None:
            return False  # not started yet
        else:
            return (smc.X.shared['batch'] >= self.maxbatch) and (
                smc.X.shared['epn'] >= 1.)

    def current_target(self):
        def func(x):
            x.lprior = self.model.prior.logpdf(x.theta)
            if x.shared['batch'] > 0:
                x.llik = self.model.loglik(x.theta, t=x.shared['batch'] - 1)
                x.lpost = x.lprior + x.llik
            else:
                x.llik = np.zeros_like(x.lprior)
                x.lpost = x.lprior.copy()
            x.llik_next = self.model.logpyt(x.theta, x.shared['batch'])
            if x.shared['epn'] > 0.0:
                x.lpost += x.shared['epn'] * x.llik_next

        return func

    def move_to_next_batch_if_needed(self, x):
        if x.shared['epn'] >= 1.:  # time for a new batch
            x.shared['batch'] += 1
            x.shared['epn'] = 0.0
            x.llik += x.llik_next
            x.llik_next = self.model.logpyt(x.theta, x.shared['batch'])

    def find_next_epn(self, x):
        f = lambda e: rs.essl(e * x.llik_next) - self.ESSrmin * x.N
        epn = x.shared['epn']
        if f(1. - epn) >= 0:
            delta = 1.0 - epn
            x.shared['epn'] = 1.  # set 1. exactly
        else:
            delta = optimize.brentq(f, 1e-12, 1. - epn)
            x.shared['epn'] = epn + delta
        return delta

    def logG_tempering(self, x, delta):
        dl = delta * x.llik_next
        x.lpost += dl
        return dl

    def logG(self, t, xp, x):
        self.move_to_next_batch_if_needed(x)
        delta = self.find_next_epn(x)
        return self.logG_tempering(x, delta)

    def _M0(self, N):
        x0 = ssps.ThetaParticles(theta=self.model.prior.rvs(size=N))
        x0.shared["batch"] = 0
        x0.shared["epn"] = 0.0
        self.current_target(x0)
        return x0

    def M(self, t, xp):
        target = self.current_target()
        return self.move(xp, target)

# TODO;
# * storing batch / epn in list
