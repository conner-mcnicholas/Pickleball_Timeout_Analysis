# pickleball_analysis
  
An analysis to quantify the impact that timeouts have on a team's success, based on:<br>
    -389 timeouts included in <br>
    -30315 rallies played over <br>
    -714 total games<br>

With raw data sourced from Alex Spancake's "pklmart" platform (www.pklmart.com):<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/pklmart_data_entry.png?raw=true)<br>

Data is stored in AWS  postgres database, pklm_prd schema:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/schema_rels.png?raw=true)<br>

Each timeout is individually scored based on the difference between the team' rallys win percentage before and after the timeout.<br>
The rallies included in the calculation for any given timeout are the rallies before and after the timeout, bounded by the closest timeouts before and after, or the beginning/ends of the game.  Example calculations are provided for a sample game below, with rallies for one particular timeout highlighted in yellow in the figure on the left.  The figure on the right is just a more detailed record of the game's progress, including the server #, sideouts, etc.  Whereas the figure on the left is a simplified view with only the rally winners depicted:<br>
Example:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/example_calc.png?raw=true)<br>

Box plot of data, including grouping by professional status:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_30_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_32_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_33_0.png?raw=true)<br>

Same result set as viewed by histograms:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_22_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_24_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_23_0.png?raw=true)<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_26_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_27_0.png?raw=true)<br>
![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_28_0.png?raw=true)<br>

Effect on a serving opponents ability to maintain unbroken point scoring streaks (note that a streak of 0 in the far left columns essentially captures the general likelihood of a serving team winning any single rally. In that sense it reflects the disadvantage of being server, considering the rate is below 50%, and an even contest would be 50/50 for each side.):<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/output_21_1.png?raw=true)<br>

Pro teams ranked by effectiveness of timeouts, where timeout score is the product of their (timeouts per game) and their (average rally win rate improvement after a timeouts), normalized from 0 to 100:<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/imgs/5_14_2024/pro_timeout_rankings.png?raw=true)<br>

![alt text](https://github.com/conner-mcnicholas/pickleball_analysis/blob/main/docs/pro_timeout_rankings.pdf?raw=true)<br>
