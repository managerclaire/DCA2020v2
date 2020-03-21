#var_continue = 0
def run_program():
    def realness():
        print("Please enter 1 to use numbers from your 2018 tax return or 2 to run a hypothetical scenario.")
        realness = int(input("Real or hypothetical? "))
        if realness == 1:
            print("Please fetch your 2018 tax return.")
        elif realness == 2:
            print("Okay, this is a hypothetical.")
        else:
            print("Error. Input not recognized.")
            return
        return realness
    def filing_status(realness):
        if realness == 1:
            fsinput = input("Did you file married filing jointly (Y/N)? ")
        else:
            fsinput = input("Is this married filing jointly (Y/N)? ")
        if fsinput == "Y":
            filingstatus = "MFJ"
        elif fsinput == "N":
            filingstatus = "S"
        else:
            print("Error. Input not recognized.")
            return
        return filingstatus
    def children(realness):
        if realness == 1:
            children = int(input("How many qualifying children do you have? "))
        else:
            children = int(input("Qualifying children: "))
        return children
    def agi(realness):
        if realness == 1:
            agi = int(input("Please enter the number in line 7 from your 2018 1040: "))
        else:
            agi = int(input("Please enter the adjusted gross income: "))
        return agi
    def net_income_tax_liability(realness,filingstatus,children,agi):
        #for the purposes of calculating net income tax liability, the bill as written adds back in the child tax credit
        if realness == 1:
            line_eleven = int(input("Please enter the value from line 11: "))
            line_twelve = int(input("Please enter the value from line 12. If blank, enter zero: "))
            line_twelve_a = int(input("Please enter the value from line 12a. If blank, enter zero: "))
            line_thirteen = line_eleven - line_twelve
            line_seventeen = int(input("Please enter the value from line 17. If blank, enter zero: "))
            nitl = line_thirteen - line_seventeen + line_twelve_a
            #print("Your net income tax liability was $",nitl)
            return nitl
        else:
            print("This calculator assumes standard deduction and no credits other than the child tax credit.")
            if filingstatus == "MFJ":
                taxable = max(0,agi - 24000)
                if taxable <= 19050:
                    tax = .1*taxable
                elif taxable <= 77400:
                    tax = 1905 + .12*(taxable-19050)
                elif taxable <= 165000:
                    tax = 1905 + .12*(77400-19050) + .22*(taxable-77400)
                elif taxable <= 315000:
                    tax = 1905 + .12*(77400-19050) + .22*(165000-77400) + .24*(taxable-165000)
                else:
                    print("Seriously? I'm not making this calculator for rich people.")
            else:
                taxable = max(0,agi - 12000)
                if taxable <= 9525:
                    tax = .1*taxable
                elif taxable <= 38700:
                    tax = 952.5+.12*(taxable-9525)
                elif taxable <= 82500:
                    tax = 952.5+.12*(38700-9525)+.22*(taxable-38700)
                elif taxable <= 157500:
                    tax = 952.5 + .12*(38700-9525)+.22*(82500-38700)+.24*(taxable-82500)
                else:
                    print("Seriously? I'm not making this calculator for rich people.")
            print("Taxable income is calculated at $",taxable)
            child_credit = children*2000
            #print("Net tax liability is calculated at $", tax)
            return tax
    def direct_cash_assistance(filingstatus,children,agi,nitl):
        if filingstatus == "MFJ":
            if agi <= 150000:
                if nitl <= 2400:
                    dca = max(1200,nitl)+500*children
                else:
                    dca = 2400+500*children
            else:
                initial_dca = 2400+500*children
                dca = initial_dca - .05*(agi-150000)
        else:
            if agi <= 75000:
                if nitl <= 1200:
                    dca = max(600,nitl)+500*children
                else:
                    dca = 1200 + 500*children
            else:
                initial_dca = 1200+500*children
                dca = max(0,initial_dca-.05*(agi-75000))
        return dca
    def maximum_diff(filingstatus,children):
        if filingstatus == "MFJ":
            fs_max = 2400
        else:
            fs_max = 1200
        child_max = children*500
        max_benefit = child_max+fs_max
        return max_benefit
    def phase_in_out(filingstatus,agi,nitl,dca,max):
        if filingstatus == "MFJ":
            if agi >150000:
                reduction = max-dca
                reason = 2
            elif dca<max:
                reduction = max-dca
                reason = 1
            else:
                reduction = 0
                reason = 3
        else:
            if agi >75000:
                reduction = max-dca
                reason = 2
            elif dca<max:
                reduction = max-dca
                reason = 1
            else:
                reduction = 0
                reason = 3
        #print(reduction)
        #print(reason)
        return [reduction,reason]
    def percent_benefit(dca,agi):
        pb = dca/agi
        pb = pb*100
        def truncate(pb):
            return int(pb*100)/100
        pb = truncate(pb)
        return pb
    def print_results(realness, filingstatus, children, agi,nitl,dca,max,reduction,reason):
        if realness == 1:
            print("These results are based on your 2018 tax return.")
            if filingstatus == "MFJ":
                print("You filed as married filing jointly.")
            else:
                print("You filed as single.")
            print("You had ",children," qualifying children.")
            print("Your adjusted gross income was $",agi)
            print("Your net income tax liability was $", nitl)
            print("Your direct cash assistance is calculated at: $", dca)
            print("Your maximum possible benefit based on filing status and number of children was $", max)
            if reduction >0:
                if reason == 2:
                    print("Your benefit was reduced by $",reduction," because you were subject to phase out limits based on adjusted gross income.")
                elif reason ==1:
                    print("Your benefit was reduced by $",reduction," because you were subject to phase in limits based on net income tax liability.")
        else:
            print("These results are based on hypothetical numbers.")
            if filingstatus == "MFJ":
                print("Filing status: married filing jointly.")
            else:
                print("Filing status: single.")
            print("Qualifying children: ", children)
            print("Adjusted gross income: $",agi)
            print("Net income tax liability: $", nitl)
            print("Direct cash assistance: $", dca)
            print("Maximum possible benefit (based on filing status and number of children): $", max)
            if reduction >0:
                if reason ==2:
                    print("The benefit was reduced by $",reduction," because it was subject to phase out limits based on adjusted gross income.")
                elif reason==1:
                    print("The benefit was reduced by $",reduction," because it was subject to phase in limits based on net income tax liability.")
    realness = realness()
    filingstatus = filing_status(realness)
    children = children(realness)
    agi = agi(realness)
    nitl = net_income_tax_liability(realness,filingstatus,children,agi)
    dca = direct_cash_assistance(filingstatus,children,agi,nitl)
    max_benefit = maximum_diff(filingstatus,children)
    list_a = phase_in_out(filingstatus,agi,nitl,dca,max_benefit)
    reduction = list_a[0]
    reason = list_a[1]
    pb = percent_benefit(dca,agi)
    print_results(realness,filingstatus,children,agi,nitl,dca,max_benefit,reduction,reason)
    print("Direct cash assistance is equal to ",pb,"% of 2018 AGI.")
    def calc_twenty(dca):
        twenty_yn = input("Would you like to calculate the percentage of the benefit based on 2020 expected gross income (Y/N)? ")
        if twenty_yn == "N":
            return
        elif twenty_yn == "Y":
            egi_twenty = int(input("Please enter the expected 2020 gross income in whole dollars: $"))
            pb2020 = dca/egi_twenty
            pb2020 = pb2020*100
            def truncate(num):
                num = int(num*100)/100
                return num
            pb2020 = truncate(pb2020)
            print("Direct cash assistance is equal to ",pb2020,"% of 2020 expected gross income.")
        else:
            print("Invalid input.")
            return
    calc_twenty(dca)
run_program()

    