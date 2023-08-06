import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse import linalg as linalg_s
import os, random, time
from scipy import linalg

class MatrixCompletion:
    """ A general class to represent a matrix completion problem

    Data members 
    ==================== 
    M:= data matrix (numpy array).
    X:= optimized data matrix (numpy array)
    out_info:= output information for the optimization (list) 


    Class methods
    ====================
    complete_it():= method to complete the matrix
    get_optimized_matrix():= method to get the solution to the problem
    get_matrix():= method to get the original matrix
    get_out():= method to get extra information on the optimization (iter
    number, convergence, objective function)

    """
    def __init__(self, X,*args, **kwargs):
        """ Constructor for the problem instance

            Inputs:
             1) X: known data matrix. Numpy array with np.nan on the unknow entries. 
                example: 
                    X = np.random.randn(5, 5)
                    X[1][3] = np.nan
                    X[0][0] = np.nan
                    X[4][4] = np.nan

        """
        # Initialization of the members
        self._M = X
        self._X = np.array(X, copy = True) #Initialize with ini data matrix
        self._out_info = []

    def get_optimized_matrix(self):
        """ Getter function to return the optimized matrix X 

            Ouput:
             1) Optimized matrix
        """
        return self._X

    def get_matrix(self):
        """ Getter function that returns the original matrix M

            Output:
            1) Original matrix M
        """
        return self._M

    def get_out(self):
        """ Getter function to return the output information 
            of the optimization

            Output:
             1) List of length 2: number of iterations and relative residual

        """
        return self._out_info


    def _ASD(self, M, r = None, reltol=1e-5, maxiter=5000):
        """
        Alternating Steepest Descent (ASD)
        Taken from Low rank matrix completion by alternating steepest descent methods
        Jared Tanner and Ke Wei
        SIAM J. IMAGING SCIENCES (2014)
        
        We have a matrix M with incomplete entries,
        and want to estimate the full matrix
        
        Solves the following relaxation of the problem:
        minimize_{X,Y} \frac{1}{2} ||P_{\Omega}(Z^0) - P_\{Omega}(XY)||_F^2
        Where \Omega represents the set of m observed entries of the matrix M
        and P_{\Omega}() is an operator that represents the observed data. 
        
        Inputs:
         M := Incomplete matrix, with NaN on the unknown matrix
         r := hypothesized rank of the matrix
        
        Usage:
         Just call the function _ASD(M)
        """
    
        # Get shape and Omega
        m, n = M.shape
        if r == None:
            r = min(m, n, 50)
    
        # Set relative error
        Omega = ~np.isnan(M)
        frob_norm_data = linalg.norm(M[Omega])
        relres = reltol * frob_norm_data
    
        # Initialize
        I, J = np.where(Omega)
        M_omega =  csc_matrix((M[Omega], (I, J)), shape=M.shape)
        U, s, V = linalg_s.svds(M_omega, r)
        S = np.diag(s)
        X = np.dot(U, S)
        Y = V
        itres = np.zeros((maxiter+1, 1)) 
    
        XY = np.dot(X, Y)
        diff_on_omega = M[Omega] - XY[Omega]
        res = linalg.norm(diff_on_omega)
        iter = 0
        itres[iter] = res/frob_norm_data 

        while iter < maxiter and res >= relres:
            
            # Gradient for X
            diff_on_omega_matrix = np.zeros((m,n))
            diff_on_omega_matrix[Omega] = diff_on_omega
            grad_X = np.dot(diff_on_omega_matrix, np.transpose(Y))
            
            # Stepsize for X
            delta_XY = np.dot(grad_X, Y)
            tx = linalg.norm(grad_X,'fro')**2/linalg.norm(delta_XY)**2
        
            # Update X
            X = X + tx*grad_X;
            diff_on_omega = diff_on_omega-tx*delta_XY[Omega]
        
            # Gradient for Y
            diff_on_omega_matrix = np.zeros((m,n))
            diff_on_omega_matrix[Omega] = diff_on_omega
            Xt = np.transpose(X)
            grad_Y = np.dot(Xt, diff_on_omega_matrix)
        
            # Stepsize for Y
            delta_XY = np.dot(X, grad_Y)
            ty = linalg.norm(grad_Y,'fro')**2/linalg.norm(delta_XY)**2
        
            # Update Y
            Y = Y + ty*grad_Y
            diff_on_omega = diff_on_omega-ty*delta_XY[Omega]
            
            res = linalg.norm(diff_on_omega)
            iter = iter + 1
            itres[iter] = res/frob_norm_data
    
        M_out = np.dot(X, Y)
    
        out_info = [iter, itres]
    
        return M_out, out_info    

    def _sASD(self, M, r = None, reltol=1e-5, maxiter=10000):
        """
        Scaled Alternating Steepest Descent (ScaledASD)
        Taken from:
        Low rank matrix completion by alternating steepest descent methods
        Jared Tanner and Ke Wei
        SIAM J. IMAGING SCIENCES (2014)
        
        We have a matrix M with incomplete entries,
        and want to estimate the full matrix
        
        Solves the following relaxation of the problem:
        minimize_{X,Y} \frac{1}{2} ||P_{\Omega}(Z^0) - P_\{Omega}(XY)||_F^2
        Where \Omega represents the set of m observed entries of the matrix M
        and P_{\Omega}() is an operator that represents the observed data. 
        
        Inputs:
         M := Incomplete matrix, with NaN on the unknown matrix
         r := hypothesized rank of the matrix
        
        Usage:
         Just call the function _sASD(M)
        """
    
    
        # Get shape and Omega
        m, n = M.shape
        if r == None:
            r = min(m, n, 50)
    
        # Set relative error
        Omega = ~np.isnan(M)
        frob_norm_data = linalg.norm(M[Omega])
        relres = reltol * frob_norm_data
    
        # Initialize
        identity = np.identity(r);
        I, J = np.where(Omega)
        M_omega =  csc_matrix((M[Omega], (I, J)), shape=M.shape)
        U, s, V = linalg_s.svds(M_omega, r)
        S = np.diag(s)
        X = np.dot(U, S)
        Y = V
        itres = np.zeros((maxiter+1, 1)) 
    
        XY = np.dot(X, Y)
        diff_on_omega = M[Omega] - XY[Omega]
        res = linalg.norm(diff_on_omega)
        iter = 0
        itres[iter] = res/frob_norm_data

        while iter < maxiter and res >= relres:
    
            # Gradient for X
            diff_on_omega_matrix = np.zeros((m,n))
            diff_on_omega_matrix[Omega] = diff_on_omega
            grad_X = np.dot(diff_on_omega_matrix, np.transpose(Y))
    
            # Scaled gradient
            scale = linalg.solve(np.dot(Y, np.transpose(Y)), identity)
            dx = np.dot(grad_X, scale) 
    
            delta_XY = np.dot(dx, Y)
            tx = np.trace(np.dot(np.transpose(dx),grad_X))/linalg.norm(delta_XY[Omega])**2
    
            # Update X
            X = X + tx*dx
            diff_on_omega = diff_on_omega-tx*delta_XY[Omega]
    
            # Gradient for Y
            diff_on_omega_matrix = np.zeros((m,n))
            diff_on_omega_matrix[Omega] = diff_on_omega
            Xt = np.transpose(X)
            grad_Y = np.dot(Xt, diff_on_omega_matrix)
    
            # Scaled gradient
            scale = linalg.solve(np.dot(Xt, X), identity)
            dy = np.dot(scale, grad_Y) 
    
            # Stepsize for Y
            delta_XY = np.dot(X, dy)
            ty = np.trace(np.dot(dy,np.transpose(grad_Y)))/linalg.norm(delta_XY[Omega])**2
    
            # Update Y
            Y = Y + ty*dy
            diff_on_omega = diff_on_omega-ty*delta_XY[Omega]
    
            # Update iteration information
            res = linalg.norm(diff_on_omega)
            iter = iter + 1
            itres[iter] = res/frob_norm_data 
    
        M_out = np.dot(X, Y)
    
        out_info = [iter, itres]
    
        return M_out, out_info

    def complete_it(self, algo_name, r = None, reltol=1e-5, maxiter=5000):
 
        """ Function to solve the optimization with the choosen algorithm 

            Input:
             1) algo_name: Algorithm name (ASD, sASD, ect)
             2) r: rank of the matrix if performing alternating algorithm
        """
        if algo_name == "ASD":
            self._X, self._out_info = self._ASD(self._M, r, reltol, maxiter)
        elif algo_name == "sASD":
            self._X, self._out_info = self._sASD(self._M, r, reltol, maxiter)
        else:
            raise NameError("Algorithm name not recognized")

class MatrixCompletionBD:		
	""" 
	A general class for matrix factorization via stochastic gradient descent

	Class members
	==================== 
	file: three column file of user, item, and value to build models


	Class methods
	====================
	train_sgd():= method to complete the matrix via sgd
	shuffle_file():= method to 'psuedo' shuffle input file in chunks
	file_split():= method to split input file into training and test set
	save_model():= save user and items parameters to text file
	validate_sgd():= validate sgd model on test set 
	build_matrix():= for smaller data build complete matrix in pandas df or numpy matrix? 
	"""


	def __init__(self,file_path,delimitter='\t',*args, **kwargs):
		 """ 
		     Object constructor
		     Initialize Matrix Completion BD object
		 """
		 self._file = file_path
		 self._delimitter = '\t'
		 self._users = dict()
		 self._items = dict()

	def shuffle_file(self,batch_size=50000):
		"""

		Shuffle line of file for sgd method, improves performance/convergence

		"""
		data = open(self._file)
		temp_file=open('temp_shuffled.txt','w')
		try:
			temp=open('backup_data_file.txt')
			temp.close()
		except:
			os.system('cp ' +self._file + ' backup_data_file.txt')
	
		temp_array=[]
		counter=0
		for line in data:
			counter+=1
			temp_array.append(line)
			if counter==batch_size : 	
				random.shuffle(temp_array)
				for entry in temp_array:
					temp_file.write(entry)
				temp_array=[]
				counter=0

		if len(temp_array)>0:
			random.shuffle(temp_array)
			for entry in temp_array:
				temp_file.write(entry)

		data.close()
		temp_file.close()
		system_string='mv temp_shuffled.txt ' + self._file 
		os.system(system_string)

	def file_split(self,percent_train=.80, train_file='data_train.csv', test_file='data_test.csv'):
		"""

		split input file randomly into training and test set for cross validation

		"""
		train=open(train_file,'w')
		test=open(test_file,'w')
		temp_file=open(self._file)
		for line in temp_file:
			if np.random.rand()<percent_train:
				train.write(line)
			else:
				test.write(line)

		train.close()
		test.close()
		print('test file written as ' + train_file)
		print('test file written as ' + test_file)
		temp_file.close()

	def train_sgd(self,dimension=6,init_step_size=.01,min_step=1e-5,reltol=.05,rand_init_scalar=1, maxiter=100,batch_size_sgd=50000,shuffle=True,print_output=False):
		
		init_time=time.time()
		alpha=init_step_size
		iteration=0
		delta_err=1
		new_mse=reltol+10
		counter=0
		ratings=[]
		
		while iteration != maxiter and delta_err > reltol :

			data=open(self._file)
			total_err=[0]
			if alpha>=min_step: alpha*=.3
			else: alpha=min_step

			for line in data:

				record=line[0:len(line)-1].split(self._delimitter)
				record[2]=float(record[2])
				# format : user, movie,5-point-ratings
				ratings.append(record[2])
				#if record[0] in self.users and record[1] in self.items :
				try:
					# do some updating
					# updates
					error=record[2]-np.dot(self._users[record[0]],self._items[record[1]])
					self._users[record[0]]=self._users[record[0]]+alpha*2*error*self._items[record[1]]
					self._items[record[1]]=self._items[record[1]]+alpha*2*error*self._users[record[0]]
					total_err.append(error**2)
				except:
					#else:
					counter+=1
					if record[0] not in self._users:
						self._users[record[0]]=np.random.rand(dimension)*rand_init_scalar
					if record[1] not in self._items:
						self._items[record[1]]=np.random.rand(dimension)*rand_init_scalar

			data.close()
			if shuffle: 
				self.shuffle_file(batch_size=batch_size_sgd)
			iteration+=1
			old_mse=new_mse
			new_mse=sum(total_err)*1.0/len(total_err)
			delta_err=abs(old_mse-new_mse)
			if print_output and iteration%10==0: 
				print ('Delta Error: %f ' % delta_err)
				
		#Printing Final Output		
		if print_output:
			print ('Iterations: %f ' % iteration)
			print ('MSE: %f ' % new_mse)
			minutes=(time.time()-init_time)/60
			print ('Total Minutes to Run: %f' % minutes)

    
	def save_model(self,user_out='user_params.txt',item_out='item_params.txt'):
		"""
		save model user and item parameters to text file	
		user_key, user_vector entries
		item_key, item_vector entries 
		"""
		users=open(user_out,'w')
		items=open(item_out,'w')
		for key in self._users:
			user_string= key+ self._delimitter + self._delimitter.join(map(str,list(self._users[key]))) + '\n'
			users.write(user_string)

		for key in self._items:
			item_string=key+ self._delimitter + self._delimitter.join(map(str,list(self._items[key]))) + '\n'
			items.write(item_string)

		users.close()
		items.close()

	## read saved model, particularly useful for fitting very large files! 
	def read_model(self,dimension=6,saved_user_params='user_params.txt',saved_item_params='item_params.txt'):
		"""
		
		Read the saved user and item parameters from text files to the item and user dictionaries
		
		"""
		#populate users:
		user_data=open(saved_user_params)
		for line in user_data:
			record=line[0:len(line)-1].split(self._delimitter)
			key=record.pop(0)
			params=np.array(map(float,record))
			self._users[key]=params

		user_data.close()

		#populate items:
		item_data=open(saved_item_params)
		for line in item_data:
			record=line[0:len(line)-1].split(self._delimitter)
			key=record.pop(0)
			params=np.array(map(float,record))
			self._items[key]=params

		item_data.close()

	def clear_model(self):
		"""
		
		clear the user and item parameters
		
		"""
		del self._items, self._users
		self._items=dict()
		self._users=dict()

	def validate_sgd(self,test_file_path):
		"""

		run model on test/validation set, returns MSE

		"""
		mse=[]
		counter=0
		test_set=open(test_file_path)
		for line in test_set: 
			record=line[0:len(line)-1].split(self._delimitter)
			record[2]=float(record[2])
			try:
				error=record[2]-np.dot(self._users[record[0]],self._items[record[1]])
				mse.append(error**2)
			except:
				counter+=1
		
		if counter>0: print('Items/Users Key Errors: %f ' % counter )
		# returns Mean Squared Error
		return sum(mse)/len(mse)

	def build_matrix(self):
		pass
