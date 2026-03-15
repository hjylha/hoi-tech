
from pathlib import Path
import csv
import time

# db/building_costs.txt
IC_COST = 6.5
IC_TIME = 380
IC_MP = 1
IC_SIZE = 1

IC_WORK = IC_COST * IC_TIME  # 2470

INFRA_COST = 1.15
INFRA_TIME = 90
INFRA_MP = 0
INFRA_SIZE = 0.05

INFRA_WORK = INFRA_COST * INFRA_TIME  # 103.5
MAX_INFRA = 40

BASE_EFFICIENCY = 0.9

MULTIPLIER = 0.005

class ICCalc:

    def __init__(
        self,
        ic_cost=IC_COST,
        ic_time=IC_TIME,
        infra_cost=INFRA_COST,
        infra_time=INFRA_TIME,
        base_efficiency=BASE_EFFICIENCY,
        multiplier=MULTIPLIER,
        efficiency_constant=int(BASE_EFFICIENCY / MULTIPLIER),
        inverse_multiplier=int(1 / MULTIPLIER),
        min_infra_for_ic_production=7,
        max_infra_num=40,
        max_years=20
    ):
        self.IC_COST = ic_cost
        self.IC_TIME = ic_time
        self.INFRA_COST = infra_cost
        self.INFRA_TIME = infra_time
        self.BASE_EFFICIENCY = base_efficiency
        self.MULTIPLIER = multiplier
        self.min_infra_for_ic_production = min_infra_for_ic_production
        self.MAX_INFRA_NUM = max_infra_num
        self.MAX_DAYS = max_years * 360
        
        self.eff_base = efficiency_constant
        self.inv_mult = inverse_multiplier
        self.ic_cost_m = int(self.IC_COST * self.inv_mult * self.inv_mult)
        self.infra_cost_m = int(self.INFRA_COST * self.inv_mult * self.inv_mult)

    def get_ic_work(self):
        return self.IC_COST * self.IC_TIME
    
    def get_ic_work_m(self):
        return self.ic_cost_m * self.IC_TIME
    
    def get_infra_work(self):
        return self.INFRA_COST * self.INFRA_TIME
    
    def get_infra_work_m(self):
        return self.infra_cost_m * self.INFRA_TIME

    def get_efficiency(self, base_ic, infra_num):
        infra_eff = self.BASE_EFFICIENCY + self.MULTIPLIER * infra_num
        return infra_eff * (1 + base_ic * self.MULTIPLIER)
        # return self.MULTIPLIER * self.MULTIPLIER * (self.BASE_EFFICIENCY / self.MULTIPLIER + infra_num) * (1 / self.MULTIPLIER + base_ic)

    def get_ic(self, base_ic, infra_num):
        return (self.BASE_EFFICIENCY + self.MULTIPLIER * infra_num) * base_ic * (1 + self.MULTIPLIER * base_ic)
        # return self.MULTIPLIER * self.MULTIPLIER * base_ic * (1 / self.MULTIPLIER + base_ic) * (self.BASE_EFFICIENCY / self.MULTIPLIER + infra_num)
    
    def get_ic_m(self, base_ic, infra_num):
        return base_ic * (self.inv_mult + base_ic) * (self.eff_base + infra_num)

    def get_ic_increase_by_infra(self, base_ic):
        return self.MULTIPLIER * base_ic * (1 + self.MULTIPLIER * base_ic)
        # return self.MULTIPLIER * self.MULTIPLIER * base_ic * (1 / self.MULTIPLIER + base_ic)

    def get_ic_increase_by_ic(self, base_ic, infra_num):
        return (self.BASE_EFFICIENCY + self.MULTIPLIER * infra_num) * (1 + self.MULTIPLIER * (1 + 2 * base_ic))
        # return self.MULTIPLIER * (self.BASE_EFFICIENCY / self.MULTIPLIER + infra_num) * (1 / self.MULTIPLIER + 1 + 2 * base_ic)
    
    def get_build_days_for_ic_and_infra(self, base_infra_num, ic_to_add, infra_to_add):
        days_to_build_infra = infra_to_add * self.INFRA_TIME
        infra_build_days = (0, days_to_build_infra)

        days_to_build_ic = ic_to_add * self.IC_TIME
        if base_infra_num >= self.min_infra_for_ic_production:
            return infra_build_days, (0, days_to_build_ic)
            # start_date_to_build_ic = 0
            # ic_building_ends_before = days_to_build_ic
        if base_infra_num + infra_to_add < self.min_infra_for_ic_production:
            return infra_build_days, (self.MAX_DAYS + days_to_build_ic, self.MAX_DAYS + days_to_build_ic + 1)
            # start_date_to_build_ic = self.MAX_DAYS
            # ic_building_ends_before = self.MAX_DAYS + 1
        # else:
        start_date_to_build_ic = (self.min_infra_for_ic_production - base_infra_num) * self.INFRA_TIME
        ic_building_ends_before = start_date_to_build_ic + days_to_build_ic
        return infra_build_days, (start_date_to_build_ic, ic_building_ends_before)
    
    def get_ic_for_every_day(self, base_ic, base_infra_num, ic_to_add, infra_to_add, last_day=None):
        last_day = last_day + 1 if last_day else self.MAX_DAYS
        # should this be checked somewhere else?
        infra_to_add = min(infra_to_add, self.MAX_INFRA_NUM - base_infra_num)

        build_days = self.get_build_days_for_ic_and_infra(base_infra_num, ic_to_add, infra_to_add)
        days_to_build_infra = build_days[0][1]
        start_date_to_build_ic, ic_building_ends_before = build_days[1]

        current_base_ic = base_ic
        current_infra_num = base_infra_num
        current_ic = self.get_ic(current_base_ic, current_infra_num)
        ic_for_every_day = []
        for day in range(last_day):

            recalculate_current_ic = False
            if day % self.INFRA_TIME == 0 and day <= days_to_build_infra:
                infra_num_add = day // self.INFRA_TIME
                current_infra_num = base_infra_num + infra_num_add
                recalculate_current_ic = True
            if (day - start_date_to_build_ic) % self.IC_TIME == 0 and day > start_date_to_build_ic and day <= ic_building_ends_before:
                ic_add = (day - start_date_to_build_ic) // self.IC_TIME
                current_base_ic = base_ic + ic_add
                recalculate_current_ic = True

            if recalculate_current_ic:
                current_ic = self.get_ic(current_base_ic, current_infra_num)
            ic_for_every_day.append(current_ic)

        return ic_for_every_day
    
    def get_ic_progress(self, max_ic_at_start=20, num_of_days=None):
        num_of_days = num_of_days if num_of_days else 2 * self.MAX_DAYS

        max_ic_to_build = num_of_days // self.IC_TIME
        max_infra_to_build = num_of_days // self.INFRA_TIME

        all_ic_progress = dict()

        for base_infra_num in range(self.MAX_INFRA_NUM + 1):
            max_infra = min(max_infra_to_build, self.MAX_INFRA_NUM - base_infra_num)
            for base_ic in range(max_ic_at_start + 1):
                ic_progress = dict()
                for infra_add in range(max_infra + 1):
                    for ic_add in range(max_ic_to_build + 1):
                        ic_progress[(ic_add, infra_add)] = self.get_ic_for_every_day(base_ic, base_infra_num, ic_add, infra_add, num_of_days - 1)
                all_ic_progress[(base_ic, base_infra_num)] = ic_progress

        return all_ic_progress
    
    def get_ic_progress_and_write_it_to_file(self, max_ic_at_start=20, num_of_days=None, filepath=None):
        num_of_days = num_of_days if num_of_days else 2 * self.MAX_DAYS
        all_ic_progress = self.get_ic_progress(max_ic_at_start, num_of_days)

        if filepath is None:
            filepath = Path(__file__).parent / "db" / f"ic_progress_for_{num_of_days}_days__ic_t_{self.IC_TIME}__infra_t_{self.INFRA_TIME}.csv"
        
        with open(filepath, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            header_row = ["starting_ic", "starting_infra", "ic_to_add", "infra_to_add"] + [f"day_{num + 1}" for num in range(num_of_days)]
            csv_writer.writerow(header_row)
            for starting_ic_n_infra, ic_progress_dict in all_ic_progress.items():
                starting_ic, starting_infra = starting_ic_n_infra
                for ic_n_infra_to_add, ic_progress in ic_progress_dict.items():
                    ic_to_add, infra_to_add = ic_n_infra_to_add
                    datarow = [str(starting_ic), str(starting_infra * 5), str(ic_to_add), str(infra_to_add)] + [str(ic) for ic in ic_progress]
                    csv_writer.writerow(datarow)

    
    def get_cumulative_ic_balance(self, base_ic, base_infra_num, ic_to_add, infra_to_add, last_day=None):
        last_day = last_day + 1 if last_day else self.MAX_DAYS
        # should this be checked somewhere else?
        infra_to_add = min(infra_to_add, self.MAX_INFRA_NUM - base_infra_num)

        build_days = self.get_build_days_for_ic_and_infra(base_infra_num, ic_to_add, infra_to_add)
        days_to_build_infra = build_days[0][1]
        start_date_to_build_ic, ic_building_ends_before = build_days[1]

        # days_to_build_infra = infra_to_add * self.INFRA_TIME
        # days_to_build_ic = ic_to_add * self.IC_TIME
        # if base_infra_num >= self.min_infra_for_ic_production:
        #     start_date_to_build_ic = 0
        #     ic_building_ends_before = days_to_build_ic
        # elif base_infra_num + infra_to_add < self.min_infra_for_ic_production:
        #     start_date_to_build_ic = self.MAX_DAYS
        #     ic_building_ends_before = self.MAX_DAYS + 1
        # else:
        #     start_date_to_build_ic = (self.min_infra_for_ic_production - base_infra_num) * self.INFRA_TIME
        #     ic_building_ends_before = start_date_to_build_ic + days_to_build_ic
        
        # print(f"ic starts: {start_date_to_build_ic}; ic ends before: {ic_building_ends_before}")

        current_base_ic = base_ic
        current_infra_num = base_infra_num
        current_ic = self.get_ic(current_base_ic, current_infra_num)
        cumulative_ic_balance = []
        cumulative_balance = 0
        for day in range(last_day):
            ic_balance_for_day = 0

            recalculate_current_ic = False
            if day % self.INFRA_TIME == 0 and day <= days_to_build_infra:
                infra_num_add = day // self.INFRA_TIME
                current_infra_num = base_infra_num + infra_num_add
                recalculate_current_ic = True
            if (day - start_date_to_build_ic) % self.IC_TIME == 0 and day > start_date_to_build_ic and day <= ic_building_ends_before:
                ic_add = (day - start_date_to_build_ic) // self.IC_TIME
                current_base_ic = base_ic + ic_add
                recalculate_current_ic = True

            # current_base_ic = max(0, min(day, ic_building_ends_before) - start_date_to_build_ic) // self.IC_TIME
            # current_infra_num = min(day, days_to_build_infra) // self.INFRA_TIME
            if recalculate_current_ic:
                current_ic = self.get_ic(current_base_ic, current_infra_num)
            ic_balance_for_day += current_ic

            if day < days_to_build_infra:
                ic_balance_for_day -= self.INFRA_COST
            if day >= start_date_to_build_ic and day < ic_building_ends_before:
                ic_balance_for_day -= self.IC_COST
            # ic_balance_for_day = round(ic_balance_for_day, 3)
            cumulative_balance += ic_balance_for_day
            # cumulative_ic_balance.append(ic_balance_for_day)
            cumulative_ic_balance.append(round(cumulative_balance, 3))
        return cumulative_ic_balance
    
    def get_cumulative_ic_balances(self, max_ic_at_start=20, num_of_days=None):
        num_of_days = num_of_days if num_of_days else 2 * self.MAX_DAYS

        max_ic_to_build = num_of_days // self.IC_TIME
        max_infra_to_build = num_of_days // self.INFRA_TIME

        all_cumulative_ic_balances = dict()

        for base_infra_num in range(self.MAX_INFRA_NUM + 1):
            max_infra = min(max_infra_to_build, self.MAX_INFRA_NUM - base_infra_num)
            for base_ic in range(max_ic_at_start + 1):
                cumulative_ic_balances = dict()
                for infra_add in range(max_infra + 1):
                    for ic_add in range(max_ic_to_build + 1):
                        cumulative_ic_balances[(ic_add, infra_add)] = self.get_cumulative_ic_balance(base_ic, base_infra_num, ic_add, infra_add, num_of_days - 1)
                all_cumulative_ic_balances[(base_ic, base_infra_num)] = cumulative_ic_balances

        return all_cumulative_ic_balances
    
    def get_cumulative_ic_balances_and_write_them_to_file(self, max_ic_at_start=20, num_of_days=None, filepath=None):
        num_of_days = num_of_days if num_of_days else 2 * self.MAX_DAYS
        all_ic_balances = self.get_cumulative_ic_balances(max_ic_at_start, num_of_days)

        if filepath is None:
            filepath = Path(__file__).parent / "db" / f"ic_balance_for_{num_of_days}_days__ic_t_{self.IC_TIME}__infra_t_{self.INFRA_TIME}.csv"
        
        with open(filepath, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            header_row = ["starting_ic", "starting_infra", "ic_to_add", "infra_to_add"] + [f"day_{num + 1}" for num in range(num_of_days)]
            csv_writer.writerow(header_row)
            for starting_ic_n_infra, ic_balances in all_ic_balances.items():
                starting_ic, starting_infra = starting_ic_n_infra
                for ic_n_infra_to_add, ic_balance in ic_balances.items():
                    ic_to_add, infra_to_add = ic_n_infra_to_add
                    datarow = [str(starting_ic), str(starting_infra * 5), str(ic_to_add), str(infra_to_add)] + [str(ic) for ic in ic_balance]
                    csv_writer.writerow(datarow)
    

    def get_optimal_ic_usage(self, base_ic, base_infra_num, last_day):
        MAX_IC_TO_BUILD = LAST_DAY // self.IC_TIME
        MAX_INFRA_TO_BUILD = LAST_DAY // self.INFRA_TIME
        max_infra = min(MAX_INFRA_TO_BUILD, self.MAX_INFRA_NUM - base_infra_num)
        best_balance = - (self.IC_COST + self.INFRA_COST) * LAST_DAY
        best_ic_and_infra = None
        for infra_add in range(max_infra + 1):
            for ic_add in range(MAX_IC_TO_BUILD):
                cumulative_balance = self.get_cumulative_ic_balance(base_ic, base_infra_num, ic_add, infra_add, LAST_DAY)
                if cumulative_balance[LAST_DAY] > best_balance:
                    best_balance = cumulative_balance[LAST_DAY]
                    best_ic_and_infra = (ic_add, infra_add)


if __name__ == "__main__":
    # FORCE INTEGERS, MULTIPLY BY 40_000
    # IC_COST = 260_000
    # IC_WORK = IC_COST * IC_TIME  # 98_800_000
    # INFRA_COST = 46_000
    # INFRA_WORK = INFRA_COST * INFRA_TIME  # 4_140_000
    # # MULTIPLY THESE BY 200
    # BASE_EFFICIENCY = 180
    # MULTIPLIER = 1

    MAX_IC = 50
    MAX_INFRA_NUM = 40

    MAX_DAYS = 20 * 360

    MAX_IC_TO_BUILD = MAX_DAYS // IC_TIME
    # MAX_INFRA_TO_BUILD = MAX_DAYS // INFRA_TIME

    # ic_calc_0 = ICCalc(IC_COST, IC_TIME, INFRA_COST, INFRA_TIME, BASE_EFFICIENCY, MULTIPLIER)
    # ic_calc = ICCalc(IC_COST, IC_TIME, INFRA_COST, INFRA_TIME, BASE_EFFICIENCY, MULTIPLIER)
    ic_calc = ICCalc()
    # INFRA_WORK_0 = ic_calc_0.get_infra_work()
    # IC_WORK_0 = ic_calc_0.get_ic_work()

    # INT_MULTIPLIER = 200
    # INT_MULTIPLIER_SQ = INT_MULTIPLIER * INT_MULTIPLIER

    # ic_calc = ICCalc(INT_MULTIPLIER_SQ * IC_COST, IC_TIME, INT_MULTIPLIER_SQ * INFRA_COST, INFRA_TIME, INT_MULTIPLIER * BASE_EFFICIENCY, INT_MULTIPLIER * MULTIPLIER)
    INFRA_WORK = ic_calc.get_infra_work()
    IC_WORK = ic_calc.get_ic_work()

    # ic_increases_by_infra = [round(get_ic_increase_by_infra(base_ic), 3) for base_ic in range(MAX_IC + 1)]
    # days_to_return_investment = []
    # cumulative_payoff_for_infras = []
    # cumulative_payoff_for_ic = dict()
    # for base_ic in range(MAX_IC + 1):
    #     # if base_ic != 0:
    #     # increase_by_infra_0 = ic_calc_0.get_ic_increase_by_infra(base_ic)
    #     increase_by_infra = ic_calc.get_ic_increase_by_infra(base_ic)
    #     cumulative_payoff = []
    #     payoff = 0
    #     for d in range(MAX_DAYS):
    #         if d < INFRA_TIME:
    #             payoff -= INFRA_COST
    #             cumulative_payoff.append(payoff)
    #             continue
    #         payoff += increase_by_infra
    #         cumulative_payoff.append(payoff)
    #     cumulative_payoff_for_infras.append(cumulative_payoff)

    #     # if increase_by_infra != INT_MULTIPLIER_SQ * increase_by_infra_0:
    #     #     print(base_ic, f"{increase_by_infra_0=}, {increase_by_infra=}")
    #     #     break
    #     # days = INFRA_WORK // increase_by_infra
    #     # extra = INFRA_WORK % increase_by_infra
    #     # if extra:
    #     #     days += 1
    #     # days_to_return_investment.append(("infra", base_ic, infra_num, days))
    #     for infra_num in range(MAX_INFRA_NUM + 1):
    #         increase_by_ic = ic_calc.get_ic_increase_by_ic(base_ic, infra_num)

    #         cumulative_payoff = []
    #         payoff = 0
    #         for d in range(MAX_DAYS):
    #             if d < IC_TIME:
    #                 payoff -= IC_COST
    #                 cumulative_payoff.append(payoff)
    #                 continue
    #             payoff += increase_by_ic
    #             cumulative_payoff.append(payoff)
    #         cumulative_payoff_for_ic[(base_ic, infra_num)] = cumulative_payoff

    #         # days = IC_WORK // increase_by_ic
    #         # extra = IC_WORK % increase_by_ic
    #         # if extra:
    #         #     days += 1
    #         # days_to_return_investment.append(("ic", base_ic, infra_num, days))

    # # days_to_return_investment = sorted(days_to_return_investment, key=lambda t: t[3])
    # # best_infra = [(t[1], t[3]) for t in days_to_return_investment if t[0] == "infra"]
    # # best_ic = [(t[1], t[2], t[3]) for t in days_to_return_investment if t[0] == "ic"]
    # when_ic_overtakes = []
    # for base_ic in range(MAX_IC + 1):
    #     when_ic_overtakes_given_infra = []
    #     for infra_num in range(MAX_INFRA_NUM + 1):
    #         for d in range(MAX_DAYS):
    #             if cumulative_payoff_for_infras[base_ic][d] < cumulative_payoff_for_ic[(base_ic, infra_num)][d]:
    #                 when_ic_overtakes_given_infra.append(d + 1)
    #                 break
    #         else:
    #             when_ic_overtakes_given_infra.append(-1)
            
    #     when_ic_overtakes.append(when_ic_overtakes_given_infra)
    

    # 33-02-01 -> 39-09-01
    # LAST_DAY = 6 * 360 + 7 * 30  # 2370 (seems low)
    # # LAST_DAY = 3000
    # MAX_IC_TO_BUILD = LAST_DAY // ic_calc.IC_TIME
    # MAX_INFRA_TO_BUILD = LAST_DAY // ic_calc.INFRA_TIME

    # # IC_TIME = 342
    # # INFRA_TIME = 81
    # IC_TIME = 380
    # INFRA_TIME = 90

    # ic_calc = ICCalc(ic_time=IC_TIME, infra_time=INFRA_TIME)

    
    # start_time = time.time()

    # best_ic_and_infra_add = dict()

    # for base_infra_num in range(8, 21):
    #     max_infra = min(MAX_INFRA_TO_BUILD, ic_calc.MAX_INFRA_NUM - base_infra_num)
    #     for base_ic in range(18):
    #         best_balance = - (ic_calc.IC_COST + ic_calc.INFRA_COST) * LAST_DAY
    #         best_ic_and_infra = None
    #         for infra_add in range(max_infra + 1):
    #             for ic_add in range(MAX_IC_TO_BUILD):
    #                 cumulative_balance = ic_calc.get_cumulative_ic_balance(base_ic, base_infra_num, ic_add, infra_add, LAST_DAY)
    #                 if cumulative_balance[LAST_DAY] > best_balance:
    #                     best_balance = cumulative_balance[LAST_DAY]
    #                     best_ic_and_infra = (ic_add, infra_add)
    #         best_ic_and_infra_add[(base_ic, base_infra_num)] = best_ic_and_infra
    
    # end_time = time.time()
    # print(f"Calculations took {round(end_time - start_time, 3)} seconds.")

    

    # filepath = Path(__file__).parent / "db" / f"optimal_building_{LAST_DAY}_days_to_build__ic_time_{IC_TIME}_infra_time_{INFRA_TIME}.csv"
    # if not filepath.exists():
    #     with open(filepath, "w") as f:
    #         writing = csv.writer(f, delimiter=";")
    #         writing.writerow(["starting_ic", "starting_infra", "ic_to_build", "infra_to_build"])
    #         for key, value in best_ic_and_infra_add.items():
    #             writing.writerow([str(key[0]), str(key[1] * 5), str(value[0]), str(value[1])])

    # print(f"{LAST_DAY // 360} years, {(LAST_DAY % 360) // 30} months and {LAST_DAY % 30} days from starting production ({LAST_DAY} days in total):")

    # print(f" ic\tinfra\t\tic more\tinfra more")
    # for key, value in best_ic_and_infra_add.items():
    #     print(f" {key[0]}\t{key[1] * 5}\t\t{value[0]}\t{value[1]}")

    start_time = time.time()

    ic_calc.get_ic_progress_and_write_it_to_file(max_ic_at_start=30, num_of_days=400)

    end_time = time.time()

    print(f"Calculated ic progress and saved to file in {round(end_time - start_time, 3)} seconds")

    start_time = time.time()

    ic_calc.get_cumulative_ic_balances_and_write_them_to_file(max_ic_at_start=30, num_of_days=400)

    end_time = time.time()

    print(f"Calculated ic balances and saved to file in {round(end_time - start_time, 3)} seconds")



    # base_ic = 10
    # base_infra_num = 20
    # infra_add = 10
    # ic_add = 0
    # last_day = 2500

    # print(f"{last_day // 360} years, {(last_day % 360) // 30} months and {last_day % 30} days from starting production ({last_day} days in total):")

    # b = ic_calc.get_cumulative_ic_balance(base_ic, base_infra_num, infra_add, ic_add, last_day)
    # print(f"{ic_calc.get_ic(base_ic, base_infra_num)} to {ic_calc.get_ic(base_ic + ic_add, base_infra_num + infra_add)} ({ic_add} ic, {infra_add} infra more)")
    # print(f"{b[0]=}, {b[380]=}, {b[400]=}, {b[last_day]=}")
    
    # print()

    # b0 = ic_calc.get_cumulative_ic_balance(base_ic, base_infra_num, 0, 0, last_day)
    # print(f"Staying at {ic_calc.get_ic(base_ic, base_infra_num)}")
    # print(f"{b0[0]=}, {b0[380]=}, {b0[400]=}, {b0[last_day]=}")


