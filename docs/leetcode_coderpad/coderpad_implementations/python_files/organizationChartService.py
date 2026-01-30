from collections import defaultdict

# - `add_employee(manager, employee)`
#     - If `manager` is `None`, `employee` is the CEO
#     - Otherwise, `employee` reports directly to `manager`
#     - You may assume inputs are valid and no duplicate employees are added
#     - Second CEO means error or ignore
# - `get_reports(manager)`
#     - Return all direct and indirect reports of `manager`
#     - Order does not matter
#     - If `manager` has no reports, return empty list
# - `lowest_common_manager(a, b)`
#     - Return the lowest (deepest) `manager` that is an ancestor of both `a` and `b`
#     - If one `employee` is the `manager` of the other, return that `manager`
#     - If either `employee` doesn’t exist, return `None`
    
class OrgChart:
    def __init__(self):
        # defaultdict come with too many issues of default values that might screw us up
        #   better to be specific and catch errors
        self.employee_to_manager = {} # defaultdict(str)
        self.manager_to_employee = {} # defaultdict(list)
        self.ceo = ""
        
    def add_employee(self, manager: str | None, employee: str) -> None:
        if employee in self.employee_to_manager.keys():
            raise ValueError(f"{employee} already exists")
        
        # fine for this to map to None if CEO
        self.employee_to_manager[employee] = manager
        if not manager:
            self.ceo = employee
            return

        self.manager_to_employee.setdefault(manager, []).append(employee)
            
    def get_reports(self, manager: str) -> list[str]:
        if manager not in self.manager_to_employee.keys():
            return([])
        
        reports = []
        
        # CEO
        #  ├─ A
        #  │   ├─ C
        #  │   └─ D 
        #          ├─ F
        #  └─ B
        #      └─ E        
        def dfs(employee: str):

            for employee in self.manager_to_employee[employee]:
                reports.append(employee)
                # if employee has directs - we know we can't delete employees
                #   so if employee exists here, they have directs
                if employee in self.manager_to_employee.keys():
                    dfs(employee)
        
        dfs(manager)
        return(reports)
    
    def lowest_common_manager(self, a: str, b: str) -> str | None:
        # check existence, CEO will still be in this dict with value of None
        if a not in self.employee_to_manager.keys() or b not in self.employee_to_manager.keys():
            return(None)

        # both employees exist at this point
        # CEO
        #  ├─ A
        #  │   ├─ C
        #  │   └─ D
        #          ├─ F
        #          ├─ Z
        #  └─ B
        #      └─ E
        # lca(a, e)
        # 
        resp = None
        def dfs(employee: str, a: str, b: str) -> int:
            nonlocal resp
            
            # if we've found sol'n already
            if resp is not None:
                return
            
            count = 0
            if employee == a:
                count += 1
            if employee == b:
                count += 1
            
            for direct_report in self.manager_to_employee.get(employee, []):
                count += dfs(direct_report)
            
            if count >= 2:
                resp = employee
            
            return(count)
            
            
            return(None)    
                
        
        # this has to start from CEO as far as I can tell
        dfs(self.ceo, a, b)
        return(resp)