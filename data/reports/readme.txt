CURRENT REPORT DATA
-------------------------------------------------------
The records found in the accompanying files are from the latest version of reports. Data from reports that have been amended has been excluded.
The data is tab-delimited.
All report items, receipts, expenditures, etc.. are in one file now, report-items.txt. They can be differentiated by their record type ID (table shown below).


REPORT TYPES
-------------------------------------------------------
Report_Type_ID	Description		Category	
10	Initial Report				Depository	
11	Year-End Report				Depository	
12	Dissolution Report			Depository	
13	External Activity Report	Depository	
14	Transition Out Report		Depository	
15	Transition In Report		Depository	
16	Legacy D102 Report			Depository	
20	Pre-primary Report			Non-Depository	
21	Pre-election Report			Non-Depository	
22	Pre-primary Report (Special) 	Non-Depository	
23	Pre-election Report (Special) 	Non-Depository	
24	Year-end Report				Non-Depository	
25	Dissolution Report			Non-Depository	
26	Post-election Report		Non-Depository	
27	Other Report				Non-Depository			Deprecated
28	Mid-year Report				Non-Depository	
29	Transition Report			Non-Depository	
30	Pre-primary Report 			Political Action Committee	
31	Pre-election Report			Political Action Committee	
32	Year-end Report				Political Action Committee	
33	Dissolution Report			Political Action Committee	
34	Other Report				Political Action Committee	Deprecated
35	Mid-year Report				Political Action Committee	
36	IEPAC Year-End Report		IEPAC	
37	IEPAC Dissolution Report	IEPAC	
40	Initial Report (BQ)			Ballot Question Committee	
41	60th Day Preceding Election Report (BQ)	Ballot Question Committee	
42	Sept 20th Report (BQ)		Ballot Question Committee	
43	Oct 5th Report (BQ)			Ballot Question Committee	
44	Oct 20th Report (BQ)		Ballot Question Committee	
45	Year-end Report (BQ)		Ballot Question Committee	
46	Dissolution Report (BQ)		Ballot Question Committee	
47	Other Report (BQ)			Ballot Question Committee	Deprecated
48	Nov 5th Report (BQ)			Ballot Question Committee	
49	Nov 20th Report (BQ)		Ballot Question Committee	
50	Pre-primary Report (WTC)	Local Party Committee	
51	Pre-election Report (WTC)	Local Party Committee	
52	Year-end Report (WTC)		Local Party Committee	
53	Dissolution Report (WTC)	Local Party Committee		Deprecated
54	Other Report (WTC)			Local Party Committee		Deprecated
55	Pre-primary Report (Special) 	Local Party Committee	
56	Pre-election Report (Special) 	Local Party Committee	
57	Post-election Report (Special) 	Local Party Committee	
110	Pre-preliminary	(M) 		Municipal	
111	Pre-election	(M) 		Municipal	
113	Year-end	(M) 			Municipal	
114	Dissolution	(M) 			Municipal	
115	Other	(M) 				Municipal			Deprecated
116	Post-election Report	(M) 	Municipal	
120	Independent Expenditure Report	Non-Registered	
121	Ballot Question Spending Report	Non-Registered	
122	Electioneering Communication Report Non-Registered	
123	Political Spending Report	Non-Registered	
60	Deposit Report			Depository
61	Late Contribution Report	BQ/Non-Dep/Dep./Muni.
62	Donation Report			Segregated Accounts
63	Subvendor Report		Depository
64	IEPAC Report			IEPAC
65	Payroll Itemization Report	Depository
66	Bank Expenditure Itemization Report	Depository
70	Bank Report, Full Month	Bank	Bank				Deprecated
71	Bank Report, First Half	Bank	Bank				Deprecated
72	Bank Report, Second Half	Bank	
80	Credit Card Report			Depository	
90	Reimbursement Report		Depository	








ITEM RECORD TYPES
-------------------------------------------------------
Each record has a record type ID
The following is a list of record types used by OCPF:

ID	Record_Type
201	Individual Contribution
202	Committee Contribution
203	Union/Association Contribution
204	Non-contribution receipt
205	Bank Interest
206	Candidate Loan
207	Transfer from Savings
208	Merchant Provider Fee (Deprecated)
209	IEPAC Transfer (In)
210	Voluntary Payroll Deduction
211	Business/Corporation Contribution
212	Refunded Merchant Provider Fee	
220	Aggregated Un-itemized Receipts
230	Donation (Segregated Funds Only)		
301	Expenditure
302	Bank Fee
303	Contribution to a registered committee
304	Liability Repayment
305	Refunded Credit Card Contribution
307	Reimbursement (with sub-items)
308	Credit Card Payment (with sub-items)
309	Vendor Payment with subvendor payments
310	Candidate Loan Repayment
311	Bank-reported expenditure
312	Bank Expenditure Itemization Item
314	Refund of Contribution
315	Independent Expenditure
316	Adminstrative Expense
317	IEPAC Transfer (Out)
319	Merchant Provider Fee
320	Aggregated Un-itemized Expenditures	
331	Out-of-pocket candidate expense (as loan)
332	Out-of-pocket candidate expense (as contribution) 	
351	Reimbursement Sub-item
352	Subvendor Sub-item (Deprecated)
354	Credit Card Sub-item	
401	Individual Inkind Contribution
402	Committee Inkind Contribution
403	Union/Association In-kind contribution
404	Loan forgiveness
405	Corporate Inkind Contribution
420	Aggregated Un-itemized In-kind contributions	
501	Liability
502	Liability incurred for an independent expenditure	
509	Liability writeoff
510	Liability settlement
517	Duplicated Candidate Loan
518	Carried Over Candidate Loan
519	Previously Reported Candidate Loan
520	Previously Reported Liability	
700	Savings Balance
701	Savings Account
720	Initial Deposit/Account Opened
721	Interest Earned
722	Transfer In
723	Other Credit	
751	Fee/Penalty
752	Transfer Out
753	Other Debit
754	Account Closed	
601	Asset Disposed (Deprecated)
801	Bank Credit
951	Subvendor Sub-item
952	Subvendor Payment (Stand-alone) Item
954	Legacy Subvendor Item (Deprecated)
955	Legacy Reimbursement Report Item (Deprecated)
956	Legacy Credit Card Charge (Deprecated)


TENDER TYPES
-------------------------------------------------------
1	Check
2	Cash or Money Order (Deprecated, use 6 or 7)
3	Credit Card
4	Transfer
5	Other
6	Cash
7	Money Order


Report Data Fields
-------------------------------------------------------
The report summary information is in the accompanying reports.txt file.
The following is a list of fields included and descriptions of each:

Report ID		The unique identifier for the report, You can see the report on our website by appending the # to the end of this url: https://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=
GUID			A globally unique identifier, used to tie amendments and amended reports together
CPF ID			The OCPF-assigned ID of the filer
Filer CPF ID		The CPF ID of the filer who filed it, different than the CPF ID when a bank report files a report on behalf of a committee, this will be the bank ID for bank reports
Report Type ID		See above for the report type
Report Type Description	A description of the report type
Is_Amendment		The report is a current version of a previously-filed report
Amendment_To_Report_ID  What report this report amended
Filing_Date		When the report was filed
Reporting Period	A description of the reporting period
Report Year		The year the report is tied to
Start Date		For reports with a multi-date reporting period, the start date
End Date		For reports with a multi-date reporting period, the end date. For reports with a single date such as deposit reports, the date
Start Balance		For reports with a start and end balance such as a year-end report, the starting balance
Receipts Total		Total of all receipts including the unitemized total
Subtotal		Start Balance + Receipts
Expenditures Total	Total of all expenditures including the unitemized total
End Balance		Start Balance + Receipts - Expenditures
Inkinds Total		Total of all inkind contributions (non-monetary) including the unitemized total
Receipts_Unitemized_Total	Total of all receipts not itemized (receipts must only be itemized if they exceed $50 annually from the same entity)
Receipts_Itemized_Total	Total of all receipts not itemized (receipts must only be itemized if they exceed $50 annually from the same entity)
Expenditures_Unitemized_Total	Total of all expenditures not itemized
Expenditures_Itemized_Total	Total of all itemized expenditures
Inkinds_Unitemized_Total	Total of all inkind (non-monetary) contributions not itemized
Inkinds_Itemized_Total	Total of all inkind (non-monetary) itemized contributions
Liabilities_Itemized_Total	Total of all liabilities outstanding as of the end date of the report
Savings_Total		Total of all savings account, only applicable for depository year-end reports
Out_Of_Pocket_Itemized_Total	A feature from deprecated reports, when candidates were allowed to spend their own funds separate from committee funds
Out_Of_Pocket_Unitemized_Total	A feature from deprecated reports, when candidates were allowed to spend their own funds separate from committee funds
Deposit_Sequence	The sequence # of the deposit, unique per filer
Reimbursee		The reimbursee, only applicable for reimbursement reports
Payments_Made		For credit card reports, how much was paid to the credit card
Interest		For credit card reports, how much interest accrued on the statement
Account_Name		For credit card reports, an abbreviation of the credit card issuer
Check_Number		For reimbursement and credit card reports
OCPF_Candidate_First_Name	The candidate name from the OCPF filer database
OCPF_Candidate_Last_Name	The candidate last name from the OCPF filer database
OCPF_Full_Name	Full name of candidate or committee (if a non-candidate filer)
OCPF_Depository_Bank_Name	The name of the depository bank of the candidate
OCPF_District_Code	The district code of the office sought of the candidate at the time the report was filed (See the district code list)
OCPF_Office		The office type description of the office sought of the candidate at the time the report was filed
OCPF_District		The district description of the office sought of the candidate at the time the report was filed
OCPF_Comm_Name		The filer's committee name at the time of filing
Payment_Date		For credit card reports, when the credit card bill was paid
In_Transit_Adjustment	For year-end depository reports, funds in transit but haven't been deposited in the bank yet
Vendor_Name		For subvendor reports only, the primary vendor



Report Item Data Fields
-------------------------------------------------------
Item_ID				The OCPF identifier of the transaction
Report_ID			The report the transaction is tied to, can be linked/join to the reports.txt list
Record_Type_ID		The record type of the transaction (see record type list above)
Date				Date of transaction
Amount				Amount of transaction
Name				Either the name (in the case of non-individuals) or the last name
First_Name			The first name, only used for individuals
Street_Address		Address info
City				Address info
State				Address info
Zip					Address info
Description			The description or purpose of the transaction, when applicable
Related_CPF_ID		If the transaction is related to a registered filer, the filer's OCPF-issued CPF ID 
Occupation			For individual contributions only, the occupation of the contributor
Employer			For individual contributions only, the employer of the contributor
Principal_Officer	For union/association contributions only, the principal officer of the entity
Tender_Type_ID		For receipts, the tender type, i.e. cash, money order or credit card
Clarified_Name		For bank-reported expenditure, this is information provided by the filer after it is filed by the bank
Clarified_Purpose	For bank-reported expenditure, this is information provided by the filer after it is filed by the bank
Is_Supported		For IEPAC expenditure and bank expenditure itemizations, whether the expenditure was spent to support or oppose the candidates
Is_Previous_Year_Receipt	True if the receipt was accepted in the previous year but deposited in the next year


