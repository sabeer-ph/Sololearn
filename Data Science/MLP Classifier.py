# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

# Load full Digits Dataset 
X,y=load_digits(n_class=10,return_X_y=True)
#Can change random state optionally
rnd_state=6
X_train,X_test,y_train,y_test=train_test_split(X,y,random_state=rnd_state)

#Training by MLP neuron_network
mlp=MLPClassifier()
mlp.fit(X_train,y_train)
print('Accuracy score: ',mlp.score(X_test,y_test).round(4))
#Create Figure : comment if run in codeplayground
nrows=2
ncols=5
fig=plt.figure(figsize=(15,6))
axis=[fig.add_subplot(nrows,ncols,x*ncols+y+1)
					  for x in range(nrows) for y in range(ncols)]
plt.suptitle('Predicted Results',size=25)

#Choice randomly 10 test cases from X_test
test_set=np.random.choice(X_test.shape[0],10)

#Show predicted numbers
print("Predict result:")
for index in range(len(test_set)):
	d_matrix=X_test[test_set[index]]
	pred_num=mlp.predict([d_matrix])[0]
	result1='{0})X_test[{1}] = {2}'.format(index,test_set[index], pred_num)
	print(result1)
	#comment codes below if run in codeplayground
	result2='X_test[{ind}] = {number}'.format(ind=test_set[index],number=pred_num)
	axis[index].matshow(d_matrix.reshape(8,8),cmap='Greys')
	axis[index].set_xlabel(result2 ,color='r',size=15)
	axis[index].set_xticks([])
	axis[index].set_yticks([])