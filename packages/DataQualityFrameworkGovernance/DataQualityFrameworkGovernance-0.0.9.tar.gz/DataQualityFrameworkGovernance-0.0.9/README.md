
  

# Data Quality Framework Governance (DQFG)

  

  

**Data Quality Framework Governance** is a structured approach to assessing, monitoring, and improving the quality of data.

  

  

An effective **Data Quality Framework** considers these dimensions and integrates them into a structured approach to ensure that data serves its intended purpose, supports informed decision-making, and maintains the trust of users and stakeholders.

  

  

**Data Quality** is an ongoing process that requires continuous monitoring, assessment, and improvement to adapt to changing data requirements and evolving business needs.

  

  

**Package structure**

  

  

**Installation:**

  

  

	pip install DataQualityFrameworkGovernance

  

**Example:** To call functions from the library.

  

  

	from Uniqueness import duplicate_rows
	print(duplicate_rows(dataframe))

  
**1. Accuracy**

  

  

-  ***accuracy_tolerance_numeric :*** Calculating data quality accuracy of a set of values (base values) by comparing them to a known correct value (lookup value) by setting a user-defined threshold percentage, applicable for numeric values.

		from  Accuracy  import  accuracy_tolerance_numeric
		print(accuracy_tolerance_numeric(dataframe, base_column, lookup_column, tolernace_percentage))

  
  

**2. Completeness**

  

  

-  ***missing_values :*** Summary of missing values in each column.

		from  Completeness  import  missing_values
		print(missing_values(dataframe))

  

-  ***overall_completeness_percentage :*** Percentage of missing values in a DataFrame. 

  
		from  Completeness  import  overall_completeness_percentage
		print(overall_completeness_percentage(dataframe))

  
**3. Consistency**

  

  

-  ***start_end_date_consistency :*** If the data in two columns is consistent, check if the "Start Date" and "End Date" column are in the correct chronological order. 

  
  		from  Consistency  import  start_end_date_consistency
		print(start_end_date_consistency(dataframe, start_date_column_name, end_date_column_name, date_format))

-  ***count_start_end_date_consistency :*** Count i	f the data in two columns is consistent, check if the "Start Date" and "End Date" column are in the correct chronological order. 

  
  		from  Consistency  import  count_start_end_date_consistency
		print(count_start_end_date_consistency(dataframe, start_date_column_name, end_date_column_name, date_format))
  
**Important**: Specify date format in *'%Y-%m-%d %H:%M:%S.%f'*  ***(It can be specified in any format, parameter value to be aligned appropriately).***
  

**4. Uniqueness**

  

  

  

-  ***duplicate_rows :*** Identify and display **duplicate** rows in a dataset. 

  
		from  Uniqueness  import  duplicate_rows
		print(duplicate_rows(dataframe))
  

-  ***unique_column_values :*** Identify and display **unique** values in a dataset. 

		from  Uniqueness  import  unique_column_values
		print(unique_column_values(dataframe, column_name))

-  ***unique_column_count :*** Identify and count **unique** values in a dataset. 

		from  Uniqueness  import  unique_column_count
		print(unique_column_count(dataframe, column_name))


**5. Validity**

-  ***validate_age :*** Validate age based on the criteria in a dataset. 

  		from  Validity  import  validate_age
		print(validate_age(dataframe, age_column, min_age, max_age))

-  ***validate_age_count :*** Count age based on the criteria in a dataset. 

  		from  Validity  import  validate_age_count
		print(validate_age_count(dataframe, age_column, min_age, max_age))
  

**Datastats**

  

  

-  ***count_rows :*** Count the number of rows in a DataFrame. 
  
  		from  Datastats  import  count_rows
		print(count_rows(dataframe))
  

  

-  ***count_columns :*** Count the number of columns in a DataFrame. 

    
  		from  Datastats  import  count_columns
		print(count_columns(dataframe))

  

-  ***count_dataset :*** Count the number of rows & columns in a DataFrame. 
    
  		from  Datastats  import  count_dataset
		print(count_dataset(dataframe))

 

  


  

  

****

  

  

**Supporting python libraries:**

  

- Pandas

  

  

****

  

[Homepage](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance)

  

  

[Bug Tracker](https://github.com/RajithPrabakaran/DataQualityFrameworkGovernance/issues)

  

  

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)