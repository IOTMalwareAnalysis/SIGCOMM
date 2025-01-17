path = "C:\\Users\\sundashr\\Source\\Repos\\IOT-Malware\\IOT-Malware\\Dataset\\csv_files\\UniqueDataSet.csv"
unique_data = read.csv(path)
summary(unique_data)

library(GGally)
ggpairs(unique_data,mapping = aes(color=Label),2:5)


iot_bulkin_wemo_sensor_mirai_dataset = read.csv("C:\\Users\\sundashr\\Source\\Repos\\IOT-Malware\\IOT-Malware\\Dataset\\csv_files\\UniqueDataSet.csv")
iot_bulkin_wemo_sensor_mirai_dataset_subset = subset(iot_bulkin_wemo_sensor_mirai_dataset, select = c("class","mean_fpktl","std_fpktl"))
head (iot_bulkin_wemo_sensor_mirai_dataset_subset)
names(iot_bulkin_wemo_sensor_mirai_dataset_subset)
binary_mirai_bulkin_subset_model_linear = svm(class ~ ., data=iot_bulkin_wemo_sensor_mirai_dataset_subset, type = 'C-classification' , kernel='linear')
summary(binary_mirai_bulkin_subset_model_linear)
attributes(binary_mirai_bulkin_subset_model_linear)
plot(binary_mirai_bulkin_subset_model_linear,iot_bulkin_wemo_sensor_mirai_dataset_subset)


summary(iot_bulkin_wemo_sensor_mirai_dataset_subset)
non_scaled = svm(class ~ ., data=iot_bulkin_wemo_sensor_mirai_dataset_subset, type = 'C-classification' , kernel='linear')
summary(non_scaled)
non_scaled$SV
non_scaled$nSV
plot(non_scaled,iot_bulkin_wemo_sensor_mirai_dataset_subset)
ggplot(data=iot_bulkin_wemo_sensor_mirai_dataset_subset, aes(x=mean_fpktl,y=std_fpktl,color=class)) + geom_point(size=2) + geom_point(data=iot_bulkin_wemo_sensor_mirai_dataset_subset[non_scaled$index,],mapping = aes(shape=class),size=5) + scale_shape_manual(values = c(5,1)) + xlim(-50,1500) + ylim(-50,1500)
abline((-coef(non_scaled)[1]/coef(non_scaled)[3]),-(coef(non_scaled)[2]/coef(non_scaled)[3]))
abline((-(coef(non_scaled)[1]-1)/coef(non_scaled)[3]),-(coef(non_scaled)[2]/coef(non_scaled)[3]),lty=2)
abline((-(coef(non_scaled)[1]+1)/coef(non_scaled)[3]),-(coef(non_scaled)[2]/coef(non_scaled)[3]), lty=2)