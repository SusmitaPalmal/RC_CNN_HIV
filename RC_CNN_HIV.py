# -*- coding: utf-8 -*-
"""CNNwithHIV1.py
"""

from keras.layers import Input,Dropout, Flatten,Dense
from sklearn.model_selection import StratifiedKFold,train_test_split
import numpy,math
from sklearn.metrics import roc_curve,auc
from keras.models import Model
from keras.utils import plot_model
from keras import initializers,regularizers,optimizers
from keras.layers.convolutional import Conv1D
import matplotlib.pyplot as plt
from keras.callbacks import LearningRateScheduler

from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score, precision_recall_curve,auc
from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import precision_score
import math
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import numpy as np
import keras
import keras.backend as K
from keras.layers import Input,Dropout, Flatten,Dense,MaxPooling1D,Activation
from keras.layers import multiply, concatenate
from sklearn.model_selection import StratifiedKFold,train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy
from sklearn.metrics import roc_curve,auc
from keras.models import Model
from keras.utils import plot_model
from keras.regularizers import l2
from keras.layers.convolutional import Conv1D
import matplotlib.pyplot as plt
import tensorflow as tf

epochs = 25

import math
def fuzzy_cal(p1,p2,p3):

    v2=p2
    v1=p1
    v3=p3


    #find the exponential of the specified value
    p1=0-((p1-1)*(p1-1)/2)
    t1=math.exp(p1)
    t1=1-t1
    m1=1-(math.tanh(((v1-1)*(v1-1))/2))
    # m1=math.tanh(p1)
    # m1=1-m1

    # print("classi1,rank1 exp",t1)
    k1=t1*m1
    # print("classi1,rank2 tan",m1,"multi",k1)

    p2=0-((p2-1)*(p2-1)/2)
    t2=math.exp(p2)
    t2=1-t2
    m2=1-(math.tanh(((v2-1)*(v2-1))/2))
    # m2=math.tanh(p2)
    # m2=1-m2
    k2=t2*m2
    # print("classi2,rank1 exp",t2)
    # print("classi2 rank2 tan",m2,"multi",k2)


    p3=0-((p3-1)*(p3-1)/2)
    t3=math.exp(p3)
    t3=1-t3
    # m3=math.tanh(p3)
    # m3=1-m3
    m3=1-(math.tanh(((v3-1)*(v3-1))/2))
    # print("classi3,rank1 exp",t3)
    k3=t3*m3
    # print("classi3 rank2 tan",m3,"mult",k3)

    # rs=(t1*m1+t2*m2+t3*m3)
    rs=k1+k2+k3
    return(rs)
# fuzzy_cal(1,2,3)

import pandas as pd


acc=0
my_auc=0
m=0
p=0
f=0


# fix random seed for reproducibility
numpy.random.seed(1)
# load  dataset
dataset1= numpy.loadtxt("/CNN-hiv1/data746/746-1200Hydrophobicity.txt", delimiter='\t')
# dataset1= numpy.loadtxt("/CNN-hiv1/data1625/4_1625_hydrophobicity_1200.txt", delimiter='\t')
# dataset1= numpy.loadtxt("/CNN-hiv1/data_schling/5_schling_hydrophobicity_1200.txt", delimiter='\t')
# dataset1= numpy.loadtxt("/CNN-hiv1/data_impense/5_impense_hydrophobicity_1200.txt", delimiter='\t')

# split into input (X) and output (Y) variables
X_Hydro = dataset1[:,0:1200]
Y = dataset1[:,1200]

dataset2= numpy.loadtxt("/CNN-hiv1/data746/4_746steric_1200.txt", delimiter='\t')
# dataset2= numpy.loadtxt("/CNN-hiv1/data1625/4_1625_steric_1200.txt", delimiter='\t')
# dataset2= numpy.loadtxt("/CNN-hiv1/data_schling/5_schling_steric_1200.txt", delimiter='\t')
# dataset2= numpy.loadtxt("/CNN-hiv1/data_impense/5_impense_steric_1200.txt", delimiter='\t')
X_Steric = dataset2[:,0:1200]

dataset3= numpy.loadtxt("/CNN-hiv1/data746/4_746polarizability_1200.txt", delimiter='\t')
# dataset3= numpy.loadtxt("/CNN-hiv1/data1625/4_1625_polarizability_1200.txt", delimiter='\t')
# dataset3= numpy.loadtxt("/CNN-hiv1/data_schling/5_schling_polarizability_1200.txt", delimiter='\t')
# dataset3= numpy.loadtxt("/CNN-hiv1/data_impense/5_impense_polarizability_1200.txt", delimiter='\t')
X_polarizability = dataset3[:,0:1200]

dataset4= numpy.loadtxt("/CNN-hiv1/data746/4_746polarity_1200.txt", delimiter='\t')
# dataset4= numpy.loadtxt("/CNN-hiv1/data1625/4_1625_polarity_1200.txt", delimiter='\t')
# dataset4= numpy.loadtxt("/CNN-hiv1/data_schling/5_schling_polarity_1200.txt", delimiter='\t')
# dataset4= numpy.loadtxt("/CNN-hiv1/data_impense/5_impense_polarity_1200.txt", delimiter='\t')

X_polarity = dataset4[:,0:1200]

dataset5= numpy.loadtxt("/CNN-hiv1/data746/4_746isoelcetric_1200.txt", delimiter='\t')
# dataset5= numpy.loadtxt("/CNN-hiv1/data1625/4_1625_isoelcetric_1200.txt", delimiter='\t')
# dataset5= numpy.loadtxt("/CNN-hiv1/data_schling/5_schling_isoelcetric_1200.txt", delimiter='\t')
# dataset5= numpy.loadtxt("/CNN-hiv1/data_impense/5_impense_isoelcetric_1200.txt", delimiter='\t')

X_isoelcetric = dataset5[:,0:1200]



AVG_SENSITIVITY=0
AVG_SPECIFICITY=0
AVG_PRECISION=0
avg_f1=0
avg_acc=0
avg_auc=0
avg_prauc=0
avgMcc=0
avgBalAcc=0

kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=1)
cvscores_clinical = []
i=1
for train_index, test_index in kfold.split(X_Hydro, Y):
			print(i,"th Fold *****************************************")

			i=i+1
			x_train_Hydro, x_test_Hydro=X_Hydro[train_index],X_Hydro[test_index]
			x_train_Hydro = numpy.expand_dims(x_train_Hydro, axis=2)
			x_test_Hydro = numpy.expand_dims(x_test_Hydro, axis=2)

			x_train_Steric, x_test_Steric=X_Steric[train_index],X_Steric[test_index]
			x_train_Steric = numpy.expand_dims(x_train_Steric, axis=2)
			x_test_Steric = numpy.expand_dims(x_test_Steric, axis=2)

			x_train_polarizability, x_test_polarizability=X_polarizability[train_index],X_polarizability[test_index]
			x_train_polarizability = numpy.expand_dims(x_train_polarizability, axis=2)
			x_test_polarizability = numpy.expand_dims(x_test_polarizability, axis=2)

			x_train_polarity, x_test_polarity=X_polarity[train_index],X_polarity[test_index]
			x_train_polarity = numpy.expand_dims(x_train_polarity, axis=2)
			x_test_polarity = numpy.expand_dims(x_test_polarity, axis=2)

			x_train_isoelcetric, x_test_isoelcetric=X_isoelcetric[train_index],X_isoelcetric[test_index]
			x_train_isoelcetric = numpy.expand_dims(x_train_isoelcetric, axis=2)
			x_test_isoelcetric = numpy.expand_dims(x_test_isoelcetric, axis=2)

			y_train, y_test = Y[train_index],Y[test_index]





			y_train_final=y_train
			y_test_final=y_test


			# CNN based on Hydrophobicity Property ========================================

			init =initializers.glorot_normal(seed=1)
			bias_init =initializers.Constant(value=0.1)
			main_input1 = Input(shape=(1200,1),name='Input')
			conv1 = Conv1D(filters=4,kernel_size=15,strides=2,activation='tanh',padding='same',name='Conv1D',kernel_initializer=init,bias_initializer=bias_init)(main_input1)
			flat1 = Flatten(name='Flatten')(conv1)
			dropout1 = Dropout(0.50)(flat1)
			dense_1= Dense(700,activation='tanh',name='dense_1',kernel_initializer=init,bias_initializer=bias_init)(flat1)
			dropout_2 = Dropout(0.25,name='dropout_2')(dense_1)
			dense1 = Dense(200,activation='tanh',name='dense1',kernel_initializer=init,bias_initializer=bias_init)(dense_1)
			dropout2 = Dropout(0.25,name='dropout2')(dense1)
			output = Dense(1, activation='sigmoid',name='output',activity_regularizer= regularizers.l2(0.01),kernel_initializer=init,bias_initializer=bias_init)(dense1)
			model = Model(inputs=main_input1, outputs=output)



			def exp_decay(epoch):
				initial_lrate = 0.001
				k = 0.1
				lrate = initial_lrate * math.exp(-k*epoch)
				return lrate
			lrate = LearningRateScheduler(exp_decay)
	    
			adams=optimizers.Adam(learning_rate=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
			model.compile(loss='binary_crossentropy', optimizer=adams, metrics=['accuracy'])
			x_train, x_val, y_train, y_val = train_test_split(x_train_Hydro, y_train, test_size=0.2,stratify=y_train)
			model.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val),callbacks=[lrate])


			scores = model.evaluate(x_test_Hydro, y_test,verbose=2)
			print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
			# cvscores.append(scores[1] * 100)
			intermediate_layer_model = Model(inputs=main_input1,outputs=dense1)
			# for extracting one layer before final layer features
			X_train_Hydro_pred = intermediate_layer_model.predict(x_train_Hydro)
			X_test_Hydro_pred = intermediate_layer_model.predict(x_test_Hydro)

			X_train=X_train_Hydro_pred
			X_test=X_test_Hydro_pred
			print(X_train.shape)


			#  CNN based on Steric Property ========================================

			model2 = Model(inputs=main_input1, outputs=output)

			model2.compile(loss='binary_crossentropy', optimizer=adams, metrics=['accuracy'])
			x_train, x_val, y_train, y_val = train_test_split(x_train_Steric, y_train_final, test_size=0.2,stratify=y_train_final)
			model2.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val),callbacks=[lrate])

			scores = model2.evaluate(x_test_Steric, y_test,verbose=2)
			print("%s: %.2f%%" % (model2.metrics_names[1], scores[1]*100))
			intermediate_layer_model = Model(inputs=main_input1,outputs=dense1)
			# for extracting one layer before final layer features
			X_train_Steric_pred = intermediate_layer_model.predict(x_train_Steric)
			X_test_Steric_pred = intermediate_layer_model.predict(x_test_Steric)

			X_train=X_train_Steric_pred
			X_test=X_test_Steric_pred
			print(X_train.shape)

			#===CNN based on polarizability Property  ========================================

			model3 = Model(inputs=main_input1, outputs=output)

			model3.compile(loss='binary_crossentropy', optimizer=adams, metrics=['accuracy'])
			x_train, x_val, y_train, y_val = train_test_split(x_train_polarizability, y_train_final, test_size=0.2,stratify=y_train_final)
			model3.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val),callbacks=[lrate])
			#model.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val))

			scores = model3.evaluate(x_test_polarizability, y_test,verbose=2)
			print("%s: %.2f%%" % (model3.metrics_names[1], scores[1]*100))

			intermediate_layer_model = Model(inputs=main_input1,outputs=dense1)
			# for extracting one layer before final layer features
			X_train_polarizability_pred = intermediate_layer_model.predict(x_train_polarizability)
			X_test_polarizability_pred = intermediate_layer_model.predict(x_test_polarizability)


			#===CNN based on polarity property========================================
			model4 = Model(inputs=main_input1, outputs=output)
			model4.compile(loss='binary_crossentropy', optimizer=adams, metrics=['accuracy'])
			x_train, x_val, y_train, y_val = train_test_split(x_train_polarity, y_train_final, test_size=0.2,stratify=y_train_final)
			model4.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val),callbacks=[lrate])
			scores = model4.evaluate(x_test_polarity, y_test,verbose=2)
			print("%s: %.2f%%" % (model4.metrics_names[1], scores[1]*100))

			intermediate_layer_model = Model(inputs=main_input1,outputs=dense1)
			# for extracting one layer before final layer features
			X_train_polarity_pred = intermediate_layer_model.predict(x_train_polarity)
			X_test_polarity_pred = intermediate_layer_model.predict(x_test_polarity)

			#CNN based on isoelcetric property========================================
			model5 = Model(inputs=main_input1, outputs=output)
			model5.compile(loss='binary_crossentropy', optimizer=adams, metrics=['accuracy'])
			x_train, x_val, y_train, y_val = train_test_split(x_train_isoelcetric, y_train_final, test_size=0.2,stratify=y_train_final)
			model5.fit(x_train, y_train, epochs=epochs, batch_size=8,verbose=2,validation_data=(x_val,y_val),callbacks=[lrate])
			scores = model5.evaluate(x_test_isoelcetric, y_test,verbose=2)
			print("%s: %.2f%%" % (model5.metrics_names[1], scores[1]*100))

			intermediate_layer_model = Model(inputs=main_input1,outputs=dense1)
			# for extracting one layer before final layer features
			X_train_isoelcetric_pred = intermediate_layer_model.predict(x_train_isoelcetric)
			X_test_isoelcetric_pred = intermediate_layer_model.predict(x_test_isoelcetric)



			#=========== Final Prediction using Stacked RF==================

			X_train=np.concatenate((X_train_Hydro_pred,X_train_Steric_pred,X_train_polarizability_pred,X_train_polarity_pred,X_train_isoelcetric_pred), axis=1)
			print(X_train.shape)
			X_test=np.concatenate((X_test_Hydro_pred,X_test_Steric_pred,X_test_polarizability_pred,X_test_polarity_pred,X_test_isoelcetric_pred ), axis=1)


			# ===========================================================================================
			cla =RandomForestClassifier(n_estimators = 200, criterion = 'entropy', random_state = 42)
			cla.fit(X_train, y_train_final)
			y_pred1 = cla.predict(X_test)
			predictions1 = cla.predict_proba(X_test)

			# ===========================================================================================
			cla =LogisticRegression(solver='lbfgs',max_iter=200)
			cla.fit(X_train, y_train_final)
			y_pred2 = cla.predict(X_test)
			predictions2 = cla.predict_proba(X_test)

			#===========================================================================================
			cla =SVC(kernel='linear',probability=True)
			cla.fit(X_train, y_train_final)
			y_pred3 = cla.predict(X_test)
			predictions3 = cla.predict_proba(X_test)


	 		#================ evaluate prediction using fuzzy score===========================
			new_Pred=[]
			# print(len(y_pred))
			for itr in range(0,len(predictions1[:,0])):
				p1=predictions1[itr,0]
				p2=predictions2[itr,0]
				p3=predictions3[itr,0]
				class1=fuzzy_cal(p1,p2,p3)
				# print(p1," ",p2," ",p3," ",class1)
				p1=predictions1[itr,1]
				p2=predictions2[itr,1]
				p3=predictions3[itr,1]
				class2=fuzzy_cal(p1,p2,p3)
				# print(p1," ",p2," ",p3," ",class2)
				if(class1<class2):
					new_Pred.append(0)
				else:
					new_Pred.append(1)


			y_pred=new_Pred
			# it is svm
			y_pred=y_pred3

			# Calculate AUC
			overall_pred=(predictions1[:,1]+predictions2[:,1]+predictions3[:,1])/3
			print("\n overall_pred ",overall_pred)
			print(y_test_final)
			auc_score = roc_auc_score(y_test_final, overall_pred)
			print("AUC score: {:.2f}".format(auc_score))

			precision, recall, _ = precision_recall_curve(y_test_final, overall_pred)
			print("precision is",precision,"\t recall is",recall)
			pr_auc_score = auc(recall, precision)

			avg_auc=avg_auc+auc_score
			avg_prauc=avg_prauc+pr_auc_score


			# Print the results
			# print("AUC score: {:.2f}".format(auc_score))
			print("my PR AUC score: {:.2f}".format(pr_auc_score))
			cm1 = confusion_matrix(y_test_final,y_pred)

			TP=cm1[1][1]
			TN=cm1[0][0]
			FP= cm1[0][1]
			FN=cm1[1][0]

			TPR = TP/(TP+FN)
			TNR = TN/(TN+FP)
			PPV =precision_score(y_test_final,y_pred)

			f1_value=(2*PPV*TPR)/(PPV+TPR)
			AVG_SENSITIVITY=AVG_SENSITIVITY+  TPR
			AVG_SPECIFICITY=AVG_SPECIFICITY+TNR
			AVG_PRECISION=AVG_PRECISION+ PPV
			avgBalAcc=avgBalAcc+(TPR+TNR)/2
			avg_f1=avg_f1+f1_value
			avg_acc=avg_acc+(TP+TN)/(TP+FP+TN+FN)
			avgMcc=avgMcc+matthews_corrcoef(y_test_final,y_pred)




			#======================================================
avg_acc=avg_acc/10
avg_acc = round(avg_acc, 3)
avgMcc=avgMcc/10
avgMcc = round(avgMcc, 3)
AVG_PRECISION=AVG_PRECISION/10
AVG_PRECISION = round(AVG_PRECISION, 3)
AVG_SENSITIVITY=AVG_SENSITIVITY/10
AVG_SENSITIVITY = round(AVG_SENSITIVITY, 3)
AVG_SPECIFICITY=AVG_SPECIFICITY/10
AVG_SPECIFICITY = round(AVG_SPECIFICITY, 3)
avgBalAcc=avgBalAcc/10
avgBalAcc = round(avgBalAcc, 3)
#AVG_PRAUC=AVG_PRAUC/10
avg_f1=avg_f1/10
avg_f1 = round(avg_f1, 3)
avg_auc=avg_auc/10
avg_auc=round(avg_auc,3)
avg_prauc=avg_prauc/10
avg_prauc=round(avg_prauc,3)

print("avg_auc,avg_prauc, Average acc, avgMcc , avg precision , AVG_SENSITIVITY, AVG_SPECIFICITY, avgBalAcc, avg f1 score ")
print(avg_auc,",",avg_prauc,",",avg_acc,",",avgMcc,",",AVG_PRECISION,",",AVG_SENSITIVITY,",",AVG_SPECIFICITY,",",avgBalAcc,",", avg_f1)

