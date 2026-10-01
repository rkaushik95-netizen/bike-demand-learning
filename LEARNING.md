# Review before using this in a portfolio

This project was prepared with assistance. It is suitable as a learning study, not proof of independent coding, a client engagement or business impact.

Explain these points in your own words:

1. Why does `groupby(['workingday', 'hr'])` answer a better question than one average over every hour?
2. Why is the denominator 499 observed working-day 17:00 records, rather than every calendar day?
3. How can a file have no null values and still have missing hours?
4. Why are 3,292,679 rentals not 3,292,679 customers?
5. What extra station-level data would make a rebalancing decision possible?
6. Why would casual + registered create target leakage in a rental-count model?
7. Why doesn't a lower mean in rainy conditions measure rain's independent effect?

Suggested next exercise: plot 2011 and 2012 separately using the same scales. Check whether the peak timing holds. If trying a forecast later, hold out later dates, compare against a simple seasonal baseline, and document the error rather than reporting an in-sample fit.

No forecast, SQL expertise, causal inference, employment experience, independent authorship or deployed business outcome should be claimed from this draft.
