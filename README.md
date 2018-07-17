# Using python to calculate MAPE(usually MAPE is used to evaluate a model)
    Let's assume that we have two excel 
    use data.xls(real data) to test totalDataPredict.xlsx(predict data) 
    (p.s. I'm so sorry that I can't provide data.xls and totalDataPredict.xlsx document, due to company's secrecy agreement)

# function usage
    extraction(df) #extract special data period
    
    getMonthValue(df) #use 0 to fill nan
                      #convert day,seasonal, year data to monthly data
                      #calculate "the real monthly data" (ex. seasonal/3=monthly, year/12=monthly)
    
    evaluation(real,pred) #calculate MAPE(MAPE=sum[ |y*-y|*100 / y ] /n)
                          #print MAPE (based on attributes in real.columns)
                          #Then you can copy it to a new excel sheet!
