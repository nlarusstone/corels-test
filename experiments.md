## bbound experiments

In our work in Python over the summer, we found that we could complete
some experiments in a reasonable amount of time but not others.  Now that
we have a C++ implementation that is more than an order of magnitude faster,
it would be valuable to try rerunning these experiments to see what happens.
Note the command run, approximate total time and machine used to run each experiment.

### tdata_R (Elaine)

On the tic-tac-toe dataset with `c = 0.001`, going from curiosity without the permutation
map to curiosity with the permutation map yields a speedup of > 100x :)

- [x] tdata_R with c = 0.001, curiosity, permutation map (< 10 s on Elaine's home MacBook Pro) **completed**

    `./bbcache -c 1 -p 1 -r 0.001 -n 100000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.01, curiosity, permutation map (~ 10 min on Elaine's home MacBook Pro) **completed**

    `./bbcache -c 1 -p 1 -r 0.01 -n 1000000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, breadth-first, permutation map, 10^9

    Incomplete result: best has length 4 after ~ 9060 s (~ 150 min), ~ 375 GB on beepbooop

    `./bbcache -b -p 1 -r 0.001 -n 1000000000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, curiosity (~ 1050 s on Elaine's home MacBook Pro; quickly finds optimal) **completed**

    `./bbcache -c 1 -p 0 -r 0.001 -n 100000 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, breadth-first (Elaine is declaring this unreasonable)

    `./bbcache -b -p 0 -r 0.001 ../data/tdata_R.out ../data/tdata_R.label`

- [x] tdata_R with c = 0.001, curious lb, permutation map, 10^8 (~ 110 s for best, ~145 s to clear queue, ~ 15 GB on beepboop) **completed**

    `./bbcache -c 2 -p 1 -r 0.001 -n 100000000 ../data/tdata_R.out ../data/tdata_R.label`

### small datasets:  bcancer, cars, haberman, monks1, monks2, monks3, votes (Elaine)

* Verified best for c = 0.03, cars, has length 2, 0.16301 (n = 1728)
* Verified best for c = 0.03, haberman, has length 0, 0.26471 (n = 306)
* Verified best for c = 0.03, monks2, has length 0, 0.32870 (n = 432)

- [x] c = 0.03, cars, permutation map, 10^8 (~ 3500 s, checks up to length 5) **completed**

    `./bbcache -b -p 1 -r 0.03 -n 100000000 ../data/cars.out ../data/cars.label`

- [x] c = 0.03, haberman, permutation map, 10^8 (~ 2082 s, checks up to length 8) **completed**

    `./bbcache -b -p 1 -r 0.03 -n 100000000 ../data/haberman.out ../data/haberman.label`

- [x] c = 0.03, monks2, permutation map, 10^8 (~ 860 s, working on length 4, ~ 40 GB on beepboop)

    `./bbcache -b -p 1 -r 0.03 -n 100000000 ../data/monks2.out ../data/monks2.label`

- [ ] c = 0.03, monks2, curiosity, permutation map, 10^8

    `./bbcache -b -p 1 -r 0.03 -n 100000000 ../data/monks2.out ../data/monks2.label`

- [x] c = 0.03, monks2, permutation map, 10^9 (~ 56775 s, checks up to length 8, ~ 230 GB on beepboop?) **completed**

    `./bbcache -b -p 1 -r 0.03 -n 1000000000 ../data/monks2.out ../data/monks2.label`

* Verified best for c = 0.02, bcancer, has length 1, 0.06832 (n = 683)
* Verified best for c = 0.02, cars, has length 3, 0.13523 (via bfs) (n = 1728)
* Best known for c = 0.02, haberman, has length 1, 0.25856 (n = 306)
* Best known for c = 0.02, monks2, has length 7, 0.315926 (via curiosity) (n = 432)

- [x] c = 0.02, bcancer, permutation map, 10^8 (~ 82 s, checks up to length 3) **completed**

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/bcancer.out ../data/bcancer.label`

- [x] c = 0.02, cars, permutation map, 10^8 (~ 11110 s, working on length 5)

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/cars.out ../data/cars.label`

- [ ] c = 0.02, cars, curiosity, permutation map, 10^8

    `./bbcache -c 1, -p 1 -r 0.02 -n 100000000 ../data/cars.out ../data/cars.label`

- [x] c = 0.02, cars, permutation map, 10^9 (~ 143280 s, checks up to length 6, ~ 105 GB on beepboop) **completed**

    `./bbcache -b -p 1 -r 0.02 -n 1000000000 ../data/cars.out ../data/cars.label`

- [x] c = 0.02, haberman, permutation map, 10^8 (~ 1000 s, working on length 5)

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/haberman.out ../data/haberman.label`

- [ ] c = 0.02, haberman, permutation map, 10^9

    `./bbcache -b -p 1 -r 0.02 -n 1000000000 ../data/haberman.out ../data/haberman.label`

- [x] c = 0.02, monks2, permutation map, 10^8 (~ 610 s, working on length 4)

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/monks2.out ../data/monks2.label`

- [x] c = 0.02, monks2, curiosity, permutation map, 10^8 (~ 12625 s, ~ 50 GB ? on beepboop)

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/monks2.out ../data/monks2.label`

- [ ] c = 0.02, monks2, permutation map, 10^9

    `./bbcache -b -p 1 -r 0.02 -n 1000000000 ../data/monks2.out ../data/monks2.label`

* Best known for c = 0.01, bcancer, has length 2, 0.05514 (n = 683)
* Best known for c = 0.01, cars, has length 7, 0.10125 (via curiosity) (n = 1728)
* Best known for c = 0.01, haberman, has length 3, 0.24242 (via bfs) (n = 306)
* Verified best for c = 0.01, monks1, has length 4, 0.04 (n = 432)
* Best known for c = 0.01, monks2, has length 18, 0.24944 (via curiosity) (n = 432)
* Verified best for c = 0.01, monks3, has length 2, 0.02 (n = 432)
* Verified best for c = 0.01, votes, has length 1, 0.05368 (n = 435)

- [x] c = 0.01, bcancer, permutation map, 10^8 (~ 1120 s, working on length 4, ~ 42 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/bcancer.out ../data/bcancer.label`

- [ ] c = 0.01, bcancer, permutation map, 10^9

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/bcancer.out ../data/bcancer.label`

- [x] c = 0.01, cars, permutation map, 10^8 (~ 2400 s, working on length 4, ~ 44 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/cars.out ../data/cars.label`

- [x] c = 0.01, cars, curiosity, permutation map, 10^8 (~ 12540 s, ~ 40 GB on beepboop)

    `./bbcache -c 1 -p 1 -r 0.01 -n 100000000 ../data/cars.out ../data/cars.label`

- [x] c = 0.01, haberman, permutation map, 10^8 (~ 630 s, working on length 4, ~ 42.1 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/haberman.out ../data/haberman.label`

- [x] c = 0.01, haberman, curiosity, permutation map, 10^8 (~ 850 s, ~ 90.4 GB on beepboop)

    `./bbcache -c 1 -p 1 -r 0.01 -n 100000000 ../data/haberman.out ../data/haberman.label`

- [x] c = 0.01, monks1, permutation map, 10^6 (~ 8 s) **completed**

    `./bbcache -b -p 1 -r 0.01 -n 1000000 ../data/monks1.out ../data/monks1.label`

- [x] c = 0.01, monks1, curiosity, permutation map, 10^4 (~ 0.1 s) **completed**

    `./bbcache -c 1 -p 1 -r 0.01 -n 10000 ../data/monks1.out ../data/monks1.label`

- [x] c = 0.01, monks2, permutation map, 10^8 (~ 550 s, working on length 4, ~ 42.4 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/monks2.out ../data/monks2.label`

- [x] c = 0.01, monks2, curiosity, permutation map, 10^7 (~ 5305 s)

    `./bbcache -c 1 -p 1 -r 0.01 -n 10000000 ../data/monks2.out ../data/monks2.label`

- [x] c = 0.01, monks3, permutation map, 10^3 (< 0.01 s) **completed**

    `./bbcache -b -p 1 -r 0.01 -n 1000 ../data/monks3.out ../data/monks3.label`

- [x] c = 0.01, monks3, curiosity, permutation map, 10^3 (< 0.01 s) **completed**

    `./bbcache -c 1 -p 1 -r 0.01 -n 1000 ../data/monks3.out ../data/monks3.label`

- [x] c = 0.01, votes, permutation map, 10^6 (~ 24 s) **completed**

    `./bbcache -b -p 1 -r 0.01 -n 1000000 ../data/votes.out ../data/votes.label`

- [x] c = 0.01, votes, curiosity, permutation map, 10^5 (~ 26 s) **completed**

    `./bbcache -c 1 -p 1 -r 0.01 -n 100000 ../data/votes.out ../data/votes.label`

### adult (Elaine)

- [ ] Check the support of rules in the adult dataset and consider re-mining

* Best known for c = 0.001 has length 4, 0.172146
* Best known for c = 0.01 has length 3, 0.203166
* Best known for c = 0.02 has length 2, 0.229189
* Best known for c = 0.03 has length 1, 0.241662
* Verified best for c = 0.04 has length 0, 0.247199

- [x] adult with c = 0.001, permutation map, 10^8 (3572 s, working on length 4, ~ 30 GB on beepboop)

    `./bbcache -b -p 1 -r 0.001 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.01, permutation map, 10^7 (375 s, working on length 4, ~ 4 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 10000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.01, permutation map, 10^8 (3917 s, working on length 4, ~ 41 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.01, curiosity, permutation map, 10^8 (~ 2900 s)

    `./bbcache -c 1 -p 1 -r 0.01 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

- [ ] adult with c = 0.01, permutation map, 10^9 (Estimate ~ 8 hrs, ~ 400 GB on beepboop)

    `./bbcache -b -p 1 -r 0.01 -n 1000000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.02, permutation map, 10^8 (5002 s, working on length 4, ~ 40 GB on beepboop)

    `./bbcache -b -p 1 -r 0.02 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

- [ ] adult with c = 0.02, permutation map, 10^9 (Estimate ~ 8 hrs, ~ 400 GB on beepboop)

    `./bbcache -b -p 1 -r 0.02 -n 1000000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.03, permutation map, 10^7 (~ 15 min, working on length 4, ~ 4.3 GB on beepboop)

    `./bbcache -b -p 1 -r 0.03 -n 10000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.03, permutation map, 10^8 (~ 5 hrs, working on length 5, ~ 40 GB on beepboop)

    `./bbcache -b -p 1 -r 0.03 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

- [ ] adult with c = 0.03, permutation map, 10^9

    `./bbcache -b -p 1 -r 0.03 -n 1000000000 ../data/adult_R.out ../data/adult_R.label`

- [x] adult with c = 0.04, permutation map, 10^8 (~ 5 hrs, checks up to length 6, ~ 5 GB on beepboop) **completed**

    `./bbcache -b -p 1 -r 0.04 -n 100000000 ../data/adult_R.out ../data/adult_R.label`

### telco

**See the rule mining section above first!**

- [ ] Try c = 0.01, curiosity, permutation map.
