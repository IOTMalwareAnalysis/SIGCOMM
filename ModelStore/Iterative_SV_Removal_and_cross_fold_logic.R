#iterative removal

library(caret) 
library(e1071)
library(GGally)

path = "C:\\Users\\sundashr\\Source\\Repos\\IOT-Malware\\IOT-Malware\\Dataset\\csv_files\\UniqueDataSet.csv"
unique_data = read.csv(path)
summary(unique_data)

all_data_path = "C:\\Users\\sundashr\\Source\\Repos\\IOT-Malware\\IOT-Malware\\Dataset\\csv_files\\AllDataSet.csv"
all_dataset = read.csv(all_data_path)
summary(all_dataset)

dim(unique_data)
dim(all_dataset)

lin_svm_cross_validation_10_fun <- function(dataset,k_cross=10) {
	print("Input Dataset dimensions ")
	print(dim(dataset))

	folds_10 <- createFolds(dataset$Label,k=k_cross)
	cross_valid_res = lapply(folds_10, function(x) {
		# start of function
		# in the next two lines we will separate the Training set into it's 10 pieces
		print("********************************************************************")
		training_fold = dataset[-x, ] # training fold =  training set minus (-) it's sub test fold
		test_fold = dataset[x, ] # here we describe the test fold individually
		# now apply (train) the classifer on the training_fold
		print(date())
		classifier = svm(formula = Label ~ .,
					   data = training_fold,
					   type = 'C-classification',
					   kernel = 'linear')
		# next step in the loop, we calculate the predictions and cm and we equate the accuracy
		# note we are training on training_fold and testing its accuracy on the test_fold
		print(date())
		y_pred = predict(classifier, newdata = test_fold[,c("mean_fpktl","mean_bpktl","std_fpktl","std_bpktl")])
		cf_matrix <- confusionMatrix(y_pred,test_fold[,c("Label")])
		print("Confusion matrix is :: ")
		print(cf_matrix)
		#accuracy <- (cf_matrix[1,1] + cf_matrix[2,2] + cf_matrix[3,3]) / (dim(test_fold)[1])

		cm = table(y_pred, test_fold[,c("Label")])
		accuracy = (cm[1,1] + cm[2,2] + cm[3,3]) / (dim(test_fold)[1])
		print(paste("Accuracy is : ",toString(accuracy)))
		return(accuracy)
		print("********************************************************************")
	})
	print(cross_valid_res)
	print(paste("Averege mean is ",mean(as.numeric(cross_valid_res))))
}
lin_svm_cross_validation_10_fun(all_dataset)
lin_svm_cross_validation_10_fun(unique_data)

date()
unique_data_set_base_model <- svm(Label ~ ., data=unique_data, type = 'C-classification' , kernel='linear')
date()
all_dataset_base_model <- svm(Label ~ ., data=all_dataset, type = 'C-classification' , kernel='linear')
date()


y_pred <- predict(all_dataset_base_model ,all_dataset[,c("mean_fpktl","mean_bpktl","std_fpktl","std_bpktl")])
cf_matrix <- confusionMatrix(y_pred,all_dataset[,c("Label")])
print(paste("Confusion matrix for iteration is"))
print(cf_matrix)

y_pred <- predict(unique_data_set_base_model ,all_dataset[,c("mean_fpktl","mean_bpktl","std_fpktl","std_bpktl")])
cf_matrix <- confusionMatrix(y_pred,all_dataset[,c("Label")])
print(paste("Confusion matrix for iteration is"))
print(cf_matrix)


svm_linear_iterative_removal_of_vecs <- function(dataset,iterations=1) {
	orig_training_set <- dataset
	prev_training_set <- orig_training_set

	prev_supp_vec_idx = list()
	prev_supp_vec = list()

	support_vec_idx_by_iter = list()
	training_set_arr_by_iter = list()

	#all_support_vecs = list()
	all_support_idx = list()
	all_training_set = list()
	iters <- c(1:iterations)
	for (iter in iters) {
		print("********************************************************************")
		print(date())
		#date()
		print(paste("Iteration ",toString(iter)))
		if(length(prev_supp_vec_idx) > 0) {
			prev_training_set <- prev_training_set[-prev_supp_vec_idx,]
		}
		print("==============================================================================")
		print("==============================================================================")
		print("==============================================================================")
		print(paste("10-FOLD CROSS VALIDATION RESULT FOR DATASET DIM",dim(prev_training_set)))
		lin_svm_cross_validation_10_fun(prev_training_set)
		print("==============================================================================")
		print("==============================================================================")
		print("==============================================================================")
		print("Training set dimensions")
		print(dim(prev_training_set))
		print(paste("Starting training linear SVM model for iteration ", toString(iter)))
		print(date())
		train_svm_model <- svm(Label ~ ., data=prev_training_set, type = 'C-classification' , kernel='linear')
		print(date())
		print(paste("End training linear SVM model for iteration ", toString(iter)))
		
		print(paste("No of support vectors",toString(train_svm_model$tot.nSV),"in iteration ", toString(iter)))
		print(paste("No of support vectors",toString(train_svm_model$nSV),"in iteration ", toString(iter)))
		prev_supp_vec_idx <- train_svm_model$index
		#print(paste("Coefficients of the hyperplane is ",coef(train_svm_model)))
		#print("Fetching coefficients for classes")
		#
        #
		#class_1_sv_idx <- c(1,train_svm_model$nSV[1])
		#class_2_sv_idx <- c(class_1_sv_idx[2]+1,class_1_sv_idx[2] + train_svm_model$nSV[2])
		#class_3_sv_idx <- c(class_2_sv_idx[2]+1,class_2_sv_idx[2] + train_svm_model$nSV[3])	
		#
		#class_1_2_coeff <-  c(train_svm_model$coefs[c(class_1_sv_idx[1]:class_1_sv_idx[2]),1],train_svm_model$coefs[c(class_2_sv_idx[1]:class_2_sv_idx[2]),1])
		#class_1_3_coeff <-  c(train_svm_model$coefs[c(class_1_sv_idx[1]:class_1_sv_idx[2]),2],train_svm_model$coefs[c(class_3_sv_idx[1]:class_3_sv_idx[2]),1])
		#class_2_3_coeff <-  c(train_svm_model$coefs[c(class_2_sv_idx[1]:class_2_sv_idx[2]),2],train_svm_model$coefs[c(class_3_sv_idx[1]:class_3_sv_idx[2]),2])
		#print(paste("Class 1-2 alpha-coefficients are of length : ", toString(dim(t(class_1_2_coeff)))))
		#print(paste("Class 2-3 alpha-coefficients are of length : ", toString(dim(t(class_2_3_coeff)))))
		#print(paste("Class 1-3 alpha-coefficients are of length : ", toString(dim(t(class_1_3_coeff)))))
        #
		##print(paste("Class 1-2 alpha-coefficients are of length : ", toString(length(class_1_2_coeff))))
		##print(paste("Class 2-3 alpha-coefficients are of length : ", toString(length(class_2_3_coeff))))
		##print(paste("Class 1-3 alpha-coefficients are of length : ", toString(length(class_1_3_coeff))))
        #
        #
		#class_1_2_sv <- train_svm_model$SV[c(class_1_sv_idx[1]:class_1_sv_idx[2],class_2_sv_idx[1]:class_2_sv_idx[2]),]
		#class_1_3_sv <- train_svm_model$SV[c(class_1_sv_idx[1]:class_1_sv_idx[2],class_3_sv_idx[1]:class_3_sv_idx[2]),]
		#class_2_3_sv <- train_svm_model$SV[c(class_2_sv_idx[1]:class_2_sv_idx[2],class_3_sv_idx[1]:class_3_sv_idx[2]),]
		#print(paste("Class 1-2 support-vectors are of length : ", toString(dim(class_1_2_sv))))
		#print(paste("Class 1-3 support-vectors are of length : ", toString(dim(class_1_3_sv))))
		#print(paste("Class 2-3 support-vectors are of length : ", toString(dim(class_2_3_sv))))
        #
        #
		#weight_class_1_2 <- (t(class_1_2_coeff) %*% class_1_2_sv )
		#weight_class_1_3 <- (t(class_1_3_coeff) %*% class_1_3_sv )
		#weight_class_2_3 <- (t(class_2_3_coeff) %*% class_2_3_sv )
		#print(paste("Class 1-2 weights are of length : ", toString(dim(weight_class_1_2))))
		#print(paste("Class 1-3 weights are of length : ", toString(dim(weight_class_1_3))))
		#print(paste("Class 2-3 weights are of length : ", toString(dim(weight_class_2_3))))
        #
		##slope_class_1_2 <- 
		##slope_class_1_3 <-
		##slope_class_2_3 <- 
		#
		##margin_class_1_2 <-  TO DO
        #
		##slope <- -(coef(train_svm_model)[2]/coef(train_svm_model)[3])
		##angle <- atan(slope)*180/pi
		
		support_vec_idx_by_iter[iter] <- list(train_svm_model$index)
		training_set_arr_by_iter[iter] <- list(prev_training_set)
		
		#all_support_vecs <- c(all_support_vecs,train_svm_model$SV)
		all_support_idx <- c(all_support_idx,train_svm_model$index)
		
		test_set <- unique_data 
		print(paste("unique-test-set size",dim(test_set)))
		y_pred <- predict(train_svm_model,test_set[,c("mean_fpktl","mean_bpktl","std_fpktl","std_bpktl")])
		cf_matrix <- confusionMatrix(y_pred,test_set[,c("Label")])
		print(paste("Confusion matrix for iteration ",toString(iter)))
		print(cf_matrix)
		
		
		
		test_set <- all_dataset 
		print(paste("alldata-test-set size",dim(test_set)))
		y_pred <- predict(train_svm_model,test_set[,c("mean_fpktl","mean_bpktl","std_fpktl","std_bpktl")])
		cf_matrix <- confusionMatrix(y_pred,test_set[,c("Label")])
		print(paste("Confusion matrix for iteration ",toString(iter)))
		print(cf_matrix)

		print(date())
		print("********************************************************************")
	}
}



svm_linear_iterative_removal_of_vecs(unique_data,5)
svm_linear_iterative_removal_of_vecs(all_dataset,5)