# Pickleball Timeout Analysis

## Quantifying the impact of calling timeouts on team performance
  
### Purpose

Using a dataset of:<br>
&emsp;- 389 timeouts within <br>
&emsp;- 30315 rallies over <br>
&emsp;- 714 games<br>

By comparing the rally win rates of teams before and after they call a timeout, this analysis has established that, on average, timeouts improve performance by roughly 8%.<br>

### Summary of Results

That relative change in rally win rate is captured by the metric "TOboost" in the table below.  Because the serving side is at a disadvantage (winning only 42% of all rallies), the suffixes _srv and _ret pertain to only serving and returning rallies, respectively.<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/total_metrics.png?raw=true)<br>

Summary statistics grouped by skill level:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/skillmetrics.png?raw=true)<br>

### Underlying Data

The raw dataset was generated by users of by Alex Spancake's "pklmart" platform. (www.pklmart.com):<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/pklmart_data_entry.png?raw=true)<br>

Data was pulled into a python3 jupyter notebook "timeout_analysis.ipynb" directly from the pklmart postgres database in AWS:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/schema_rels.png?raw=true)<br>

### Scope & Assumptions

Each timeout is individually scored based on the difference between the team that called it's rally win % before and after the timeout.<br>

The rallies included in the calculation for any given timeout are rallies in the game (not match) before and after the timeout, bounded by any other timeouts.  This bounding was applied because other timeouts are opportunities to change strategy, and thus counteract the impact of the timeout at hand.<br>

Example calculations are provided for a sample game below, with rallies for one particular timeout highlighted in yellow in the figure on the left.<br>

The figure on the right is just a more detailed record of the game's progress, including the server #, sideouts, etc.  Whereas the figure on the left is a simplified view with only the rally winners depicted:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/example_calc.png?raw=true)<br>

### Plots

Histogram of rally win rate increases across all timeouts:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_22_0.png?raw=true)<br>

If we filter rallies to only those in which the timeout-calling team was serving:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_24_0.png?raw=true)<br>

Again, but filtering by receiving rallies instead of serving:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_23_0.png?raw=true)<br>

The following 3 charts corresond to the same set of results as the 3 preceding charts, grouped by player skill level (using DUPR rating for amateurs).<br>

All rallies:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_26_0.png?raw=true)<br>

Serving rallies:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_27_0.png?raw=true)<br>

Receiving rallies:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_28_0.png?raw=true)<br>

The same results depicted in the 3 immediately preceding charts from the perspective of box plots:<br>

All rallies:
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_30_0.png?raw=true)<br>

Serving rallies:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_32_0.png?raw=true)<br>

Receiving rallies:<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_33_0.png?raw=true)<br>


The charts below quantify the effect of timeouts on unbroken point scoring streaks, i.e. consecutive rallies won by serving team.<br> 

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_21_1.png?raw=true)<br>

Note that rate of 0-length servin win streaks, depicted in the far left columns, essentially reflects the disadvantage of being server, considering this amounts to the percentage of all rallies won by the serving team, and it turns out to be below 50%.<br>

The table below ranks pro doubles teams effectiveness of timeouts, where timeout score is the product of their [timeouts per game] and their [average rally win rate improvement after a timeouts], normalized from 0 to 100:<br>

![See PDF version for clearer rendering](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/docs/pro_timeout_rankings.pdf)<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/pro_timeout_rankings.png?raw=true)<br>