import numpy as np
from scipy.special import betaln, logsumexp,betainc
from scipy.stats import beta as beta_dist
from scipy.integrate import quad

__version__ = "0.1.1"


def log_subtract(x,y):
	if isinstance(x,float):
		assert isinstance(y,float), "If x is float y must also be float."
		assert x>=y,"X must be at least as large as y"
	else:
		assert len(x)==len(y), "X and Y must be the same length"
		assert sum(x < y)==0,"X is not larger than Y at all elements."

	results=np.zeros(x.shape)
	results[x==y]=-np.inf
	results[x!=y]=x[x!=y] + np.log1p(-np.exp(y[x!=y]-x[x!=y]))

	return results

class PiecewiseBeta:


	def __init__(self,cut_points,alpha_p,beta_p):
		"""Simple class for a piecewise beta distribution, where a beta distribution is broken into contiguous pieces with break points determined by cut_points. Note, both lower and upper ends of the full interval are assumed to be included. Therefore, cut_points specifies a total of len(cut_points)-1 discrete intervals. 
		
		Args:
		    cut_points (list or array of floats): Breakpoints for the piecewise distribution. Note, the upper and lower ends of intervals must be included. 
		    alpha_p (float): alpha prior for the underlying beta distribution
		    beta_p (float): beta prior for the underlying beta distribution
		"""
		self.cut_points=np.array(cut_points)
		self.alpha_p=alpha_p
		self.beta_p=beta_p


	def _beta_dist_piecewise_integral(self,a, b):
		expectation_integral=beta_dist(a,b).logcdf(self.cut_points[1:])+betaln(a,b)
		return np.concatenate([expectation_integral[0:1],log_subtract(expectation_integral[1:],expectation_integral[:-1])])

	def _beta_dist_piecewise_integral_single_entry(self,a, b,piece_index):
		if piece_index==0:
			return np.log(betainc(a,b,self.cut_points[1:][0]))+betaln(a,b)
		low= np.log(betainc(a,b,self.cut_points[1:][piece_index-1]))+betaln(a,b)
		target=np.log(betainc(a,b,self.cut_points[1:][piece_index]))+betaln(a,b)
		return log_subtract(target,low)

	def Mean(self,piecewise_weights):
		"""Returns the mean of the Piecewise-Beta Distribution
		
		Args:
		    piecewise_weights (list or array): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		
		Returns:
		    float: mean or expected value of distribution
		"""
		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf


		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)

		expectation_integral=self._beta_dist_piecewise_integral(self.alpha_p+1,self.beta_p)

		mean_per_interval=expectation_integral-prior_norm_constants

		return np.exp(logsumexp(log_piecewise_weights+mean_per_interval))


	def MarginalLogLikelihood(self,piecewise_weights,success, total):
		""" Given vector of piecewise-weights, computes the marginal likelihood for a set of bernoulli trials defined.  Success indicates the number of positive outcomes, total definces the total number. 
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float:  marginal log-likelihood
		"""
		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."


		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success

		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)

		expectation_integral=self._beta_dist_piecewise_integral(self.alpha_p+success,self.beta_p+failures)

		return logsumexp(log_piecewise_weights+(expectation_integral-prior_norm_constants))




	def PerPiecePosterior(self,piecewise_weights,success, total):
		""" Given an observed set of bernoulli outcomes, compute a posterior distribution over which piece the sample was generated from.
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    np.array: Vector of posterior probabilities
		"""
		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success

		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)
		expectation_integral=self._beta_dist_piecewise_integral(self.alpha_p+success,self.beta_p+failures)

		return np.exp((log_piecewise_weights+(expectation_integral-prior_norm_constants))-logsumexp(log_piecewise_weights+(expectation_integral-prior_norm_constants)))


	def PosteriorMean(self,piecewise_weights,success, total):
		"""Given an observed set of bernoulli outcomes, compute the posterior expectation of the piecewise beta distribution. 
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: posterior expectation
		"""

		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."


		failures=total-success
		per_piece_posterior=self.PerPiecePosterior(piecewise_weights,success, total)

		log_per_piece_posterior=np.zeros(per_piece_posterior.shape[0])
		log_per_piece_posterior[per_piece_posterior!=0.0]=np.log(per_piece_posterior[per_piece_posterior!=0.0])
		log_per_piece_posterior[per_piece_posterior==0.0]=-np.inf

		posterior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p+success,self.beta_p+failures)

		expectation_integral=self._beta_dist_piecewise_integral(self.alpha_p+success+1.0,self.beta_p+failures)

		mean_per_interval=np.zeros(expectation_integral.shape[0])
		mean_per_interval[expectation_integral==-np.inf]=-np.inf
		mean_per_interval[expectation_integral!=-np.inf]=expectation_integral[expectation_integral!=-np.inf]-posterior_norm_constants[expectation_integral!=-np.inf]
		return np.exp(logsumexp(log_per_piece_posterior+mean_per_interval))

	def PosteriorLogPDF(self,x,piecewise_weights,success, total):
		"""Computes the log-PDF of the posterior distribution.
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: log-density
		"""

		assert x<=1.0 and x>=0.0, "x must be between 0 and 1."

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success
		log_norm_const=self.MarginalLogLikelihood(piecewise_weights,success, total)
		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)

		piece=np.where(x<=self.cut_points[1:])[0][0]


		# segment_norm_const=self._beta_dist_piecewise_integral_single_entry(self.alpha_p+success,self.beta_p+failures,piece)

		if (x>=0.0) and (x<=1.0):
			return np.log(x)*(self.alpha_p+success-1.0)+np.log(1.0-x)*(self.beta_p+failures-1.0)+log_piecewise_weights[piece]-prior_norm_constants[piece]-log_norm_const
		else:
			return log_piecewise_weights[piece]-log_norm_const

	def PosteriorPDF(self,x,piecewise_weights,success, total):
		"""Computes the PDF of the posterior distribution.
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: density
		"""

		return np.exp(self.PosteriorLogPDF(x,piecewise_weights,success, total))

	def _fast_posterior_pdf_segment(self, x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const):
		if (x>=0.0) and (x<=1.0):
			return np.exp(np.log(x)*(self.alpha_p+success-1.0)+np.log(1.0-x)*(self.beta_p+failures-1.0)+log_piecewise_weight-log_prior_norm_const-log_norm_const)
		else:
			return np.exp(log_piecewise_weight-log_prior_norm_const-log_norm_const)

	def _fast_posterior_entropy_segment(self, x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const):
		if (x>=0.0) and (x<=1.0):
			log_pdf=np.log(x)*(self.alpha_p+success-1.0)+np.log(1.0-x)*(self.beta_p+failures-1.0)+log_piecewise_weight-log_prior_norm_const-log_norm_const
		else:
			log_pdf=log_piecewise_weight-log_prior_norm_const-log_norm_const

		return -1.0*log_pdf*np.exp(log_pdf)

	def _fast_posterior_log_x_exp(self,x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const):
		return np.log(x)*self._fast_posterior_pdf_segment(x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const)


	def _fast_posterior_log_1mx_exp(self,x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const):
		return np.log(1.0-x)*self._fast_posterior_pdf_segment(x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const)

	def _fast_posterior_exp_x(self,x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const):
		return x*self._fast_posterior_pdf_segment(x,success, failures, log_prior_norm_const,log_piecewise_weight,log_norm_const)


	def PosteriorEntropy(self,piecewise_weights,success, total):
		"""Computes the differential entropy of the posterior distribution using adaptive quadrature (QUADPACK)
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: differential entropy
		"""
		

		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success

		global_norm_const=self.MarginalLogLikelihood(piecewise_weights,success, total)
		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)


		entropy_per_segment=np.zeros(self.cut_points.shape[0]-1)
		for i in range(self.cut_points.shape[0]-1):
			if np.isfinite(log_piecewise_weights[i]):
				entropy_func=lambda x:self._fast_posterior_entropy_segment(x,success, failures, prior_norm_constants[i],log_piecewise_weights[i],global_norm_const)
				entropy,error=quad(entropy_func,self.cut_points[i],self.cut_points[i+1],limit=100,epsabs=1e-9)
				entropy_per_segment[i]=entropy
		return np.sum(entropy_per_segment)
	
	def PosteriorExpLogX(self,piecewise_weights,success, total):
		"""Computes the posterior expectatation of log(x) using adaptive quadrature (QUADPACK)
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: Posterior expectation of log(x)
		"""
		

		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success

		global_norm_const=self.MarginalLogLikelihood(piecewise_weights,success, total)
		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)


		expectation_per_segment=np.zeros(self.cut_points.shape[0]-1)
		for i in range(self.cut_points.shape[0]-1):
			exp_func=lambda x:self._fast_posterior_log_x_exp(x,success, failures, prior_norm_constants[i],log_piecewise_weights[i],global_norm_const)
			expectation,error=quad(exp_func,self.cut_points[i],self.cut_points[i+1],limit=100,epsabs=1e-9)
			expectation_per_segment[i]=expectation
		return np.sum(expectation_per_segment)
	

	def PosteriorExpLog1mX(self,piecewise_weights,success, total):
		"""Computes the posterior expectatation of log(1-x) using adaptive quadrature (QUADPACK)
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.
		    success (int): # of successes
		    total (int): # of trials
		
		Returns:
		    float: Posterior expectation of log(1-x)
		"""

		assert len(piecewise_weights)==(len(self.cut_points)-1), "Weights for each piece must equal the number of categories defined by self.cut_points."
		piecewise_weights=piecewise_weights/np.sum(piecewise_weights)
		assert total>=success,"Total number of trials must be equal or greater than the number of successes."

		piecewise_weights=np.array(piecewise_weights)
		log_piecewise_weights=np.zeros(piecewise_weights.shape[0])
		log_piecewise_weights[piecewise_weights!=0.0]=np.log(piecewise_weights[piecewise_weights!=0.0])
		log_piecewise_weights[piecewise_weights==0.0]=-np.inf

		failures=total-success

		global_norm_const=self.MarginalLogLikelihood(piecewise_weights,success, total)
		prior_norm_constants=self._beta_dist_piecewise_integral(self.alpha_p,self.beta_p)


		expectation_per_segment=np.zeros(self.cut_points.shape[0]-1)
		for i in range(self.cut_points.shape[0]-1):
			exp_func=lambda x:self._fast_posterior_log_1mx_exp(x,success, failures, prior_norm_constants[i],log_piecewise_weights[i],global_norm_const)
			expectation,error=quad(exp_func,self.cut_points[i],self.cut_points[i+1],limit=100,epsabs=1e-9)
			expectation_per_segment[i]=expectation
		return np.sum(expectation_per_segment)

		

	def RandomVariates(self,piecewise_weights,num_samples):
		""" Generates a random sample from the piecewise beta distribtion defined by the prior parameters and the piecewise_weights.
		
		Args:
		    piecewise_weights (np.array or list of floats): Defines a weighted distribution over the beta distribution pieces. Must sum to 1.

		    num_samples (int): number of samples
		
		Returns:
		    np.array: vector of samples
		"""
		cdf_vals=betainc(self.alpha_p,self.beta_p,self.cut_points)
		piece_samples=np.random.choice(np.arange(self.cut_points.shape[0]-1),size=num_samples,p=piecewise_weights)

		lower_bound=cdf_vals[piece_samples]
		upper_bound=cdf_vals[piece_samples+1]

		samples=beta_dist(self.alpha_p,self.beta_p).ppf(np.random.uniform(low=lower_bound,high=upper_bound))
		return samples

if __name__=='__main__':
	symptom_frequency_cut_points=[0.0,0.04,0.3,0.8,0.99,1.0]

	test_weights_matched=[0.04,0.26,0.5,0.19,0.01]
	test_weights_uni=[0.2,0.2,0.2,0.2,0.2]
	test_weights_non_uni=np.array([0.17296799, 0.4904317 , 0.2828488 , 0.05144387, 0.00230764])
	test_weights_non_uni/=np.sum(test_weights_non_uni)
	self=PiecewiseBeta(symptom_frequency_cut_points,1.0,1.0)

