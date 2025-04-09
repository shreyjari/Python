import pandas as pd

DocumentationDraft = "Here is the documentation structured for an Azure DevOps Wiki page with math formulas included:

---

# Operational Rate Card Documentation

## Overview

The **Operational Rate Card** is designed to calculate the fully burdened rate, total hourly costs, and the client bill rate for various PTAG positions. This document breaks down the key components of the rate card into different sections: Payroll Burdens, Fixed Costs, Optional Costs, and Margin Analysis.

## 1. Payroll Burdens

This section calculates the total payroll-related costs, including vacation days, sick/personal days, statutory holidays, and fringe benefits.

### 1.1 Program Duration - Years
- **Formula**: `= 'Input Form'!C21`
- **Explanation**: Refers to the total duration of the program in years.

### 1.2 Hours/Year
- **Formula**: `= 52 * 40`
- **Explanation**: Assumes a standard 40-hour work week for 52 weeks, leading to 2080 hours per year.

### 1.3 Vacation Days
- **Days**: `15`
- **Hours**: `= E17 * 8`
- **Hourly Cost**: `= (F17) / YearlyBillableHours_Proposal`
- **Explanation**: Calculates the hourly cost of vacation days.

### 1.4 Sick/Personal Days
- **Days**: `3`
- **Hours**: `= E18 * 8`
- **Hourly Cost**: `= (F18) / YearlyBillableHours_Proposal`
- **Explanation**: Calculates the hourly cost of sick/personal days.

### 1.5 Statutory Holidays
- **Days**: `11`
- **Hours**: `= E19 * 8`
- **Hourly Cost**: `= (F19) / YearlyBillableHours_Proposal`
- **Explanation**: Calculates the hourly cost of statutory holidays.

### 1.6 Total Payroll Burdens
- **Total Hours**: `= VacationDays_Proposal + SickDaysHours_Proposal + StatHolidaysHours_Proposal`
- **Total Costs**: `= SUM(G17:G19)`
- **Explanation**: Sum of vacation, sick/personal, and statutory holiday hours and costs.

### 1.7 Billable Hours (YearlyBillableHours)
- **Formula**: `= G16 - F20`
- **Explanation**: Total hours available for billing after accounting for vacation, sick, and statutory holidays.

### 1.8 Billable FTE Eq
- **Formula**: `= G21 / G16`
- **Explanation**: Full-time equivalent (FTE) calculation.

### 1.9 Hours Conversion Rate
- **Formula**: `= G16 / G21`
- **Explanation**: Conversion rate from total hours to billable hours.

## 2. Fringe Benefits

This section covers the costs of fringe benefits like medical, dental, life insurance, etc.

### 2.1 Company Benefits Plan (CDN)
- **Family Dental**: `= 60`
- **Medical**: `= 169.15`
- **Basic Life**: `= 20`
- **Dependent Life**: `= 4.25`
- **AD&D**: `= 2`
- **Critical Illness**: `= 29.75`
- **LTD**: `= 62.78`
- **Other**: `= 52.07`
- **Total Benefits**: `= SUM(E35:E42)`

### 2.2 Yearly Fringe Benefits Cost
- **Formula**: `= E43 * 12`
- **Hourly Cost**: `= E45 / YearlyBillableHours_Proposal`
- **Explanation**: Annual and hourly costs for fringe benefits.

## 3. Fixed Costs

Fixed costs are consistent expenses incurred over time, such as personal protective equipment (PPE) and technology costs.

### 3.1 PPE Costs
- **Formula**: `= SUM(D60:D68)`
- **Per Hour**: `= SUM(E60:E68)`
- **Explanation**: Calculates PPE costs per FTE based on items like vests, hard hats, gloves, and boots.

### 3.2 Technology Costs
- **Current FTE**: `= TotalFTE_Proposal`
- **FTE Used for Pricing**: `= +D73 * E72`
- **Computers**: `= 1000`
- **Printers**: `= D76 * $E$72`
- **Cell Phones**: `= 1200`
- **Total Costs**: `= SUM(E74:E77)`
- **Hourly Rate**: `= (E78 / TotalBillableHours_with_FTE_Proposal) / 2`
- **Explanation**: Distribution of technology costs over the project duration.

### 3.3 PTAG Onboarding & PD/Training
- **PTAG Onboarding**: `= 16 hours per year`
- **PD/Training Cost**: `= 1500 / YearlyBillableHours_Proposal`
- **Explanation**: Onboarding and training costs on an hourly basis.

## 4. Optional Costs

Optional costs include additional project-related expenses like mobilization/demobilization, per diem, vehicle costs, and project tools.

### 4.1 Mob/Demob Costs
- **Mobilization**: `= 3500`
- **Demobilization**: `= 3500`
- **Total Cost**: `= D100 * D90`
- **Mob/Demob per Person**: `= D101 / D105`
- **Explanation**: Calculations for mobilization and demobilization costs per person.

### 4.2 Per Diem Costs
- **Lodging**: `= 198`
- **Meals & Incidentals**: `= 59`
- **30-day Per Diem**: `= (D113 + D114) * D115`
- **Total Cost**: `= D121 * D116`
- **Explanation**: Per diem costs for lodging, meals, and incidentals for the duration of the project.

### 4.3 Vehicle Costs
- **Truck**: `= 125 per month`
- **Maintenance & Gas**: `= 80 per month`
- **Total Cost**: `= SUM(D133:D134)`
- **Mileage Reimbursement**: `= +D134 * D136`
- **Explanation**: Monthly vehicle costs and mileage reimbursement.

### 4.4 Project Tools Costs
- **P6 License**: `= 172 * 12`
- **FM License**: `= 100 * 12`
- **Cleo - Estimating**: `= 5875`
- **Cleo - Cost**: `= 4200`
- **MS365**: `= 1200`
- **Acumen (Deltek)**: `= 9000 + 1800`
- **@Risk**: `= 2225`
- **Total Costs**: `= SUM(F153:F161)`
- **Hourly Rate**: `= F162 / TotalBillableHours_with_FTE_Proposal`
- **Explanation**: Cost of software tools distributed over the project duration.

## 5. Margin Analysis

Margin analysis evaluates the profitability of the project by analyzing net and gross margins.

### 5.1 Net Margin ($)
- **Formula**: `= +[@[Client Bill Rate ($)]] - [@[Total Hourly Costs]]`
- **Explanation**: Difference between client bill rate and total hourly costs, representing net profit per hour.

### 5.2 Net Margin (%)
- **Formula**: `= +IFERROR([@[Net Margin ($)]] / [@[Client Bill Rate ($)]], 0)`
- **Explanation**: Net margin as a percentage of the client bill rate.

### 5.3 Gross Margin ($)
- **Formula**: `= +[@[Client Bill Rate ($)]] - [@[Negotiated Pay Rate Per Hour]]`
- **Explanation**: Difference between client bill rate and negotiated pay rate, representing gross profit per hour.

### 5.4 Gross Margin (%)
- **Formula**: `= +IFERROR([@[Gross Margin ($)]] / [@[Client Bill Rate ($)]], 0)`
- **Explanation**: Gross margin as a percentage of the client bill rate.

### 5.5 Markup Factor
- **Formula**: `= +IFERROR((([@[Client Bill Rate ($)]] - [@[Negotiated Pay Rate Per Hour]]) / [@[Negotiated Pay Rate Per Hour]]) + 1, 0)`
- **Explanation**: Factor by which the negotiated pay rate is marked up to arrive at the client bill rate.

---

This structured documentation provides a comprehensive breakdown of each section of the Operational Rate Card with formulas and explanations, making it suitable for an Azure DevOps Wiki page."