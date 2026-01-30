---
title: Template
category: Implementations
difficulty: Advanced
show_back_link: true
---

## Initial Problem Statement
You’re building an in-memory organization chart

Each employee has at most one manager (except the CEO)

The org forms a tree (no cycles)

### API
```python
class OrgChart:
    def add_employee(self, manager: str | None, employee: str) -> None
    def get_reports(self, manager: str) -> list[str]
    def lowest_common_manager(self, a: str, b: str) -> str | None
```

### Semantics
- `add_employee(manager, employee)`
    - If `manager` is `None`, `employee` is the CEO
    - Otherwise, `employee` reports directly to `manager`
    - You may assume inputs are valid and no duplicate employees are added
- `get_reports(manager)`
    - Return all direct and indirect reports of `manager`
    - Order does not matter
    - If `manager` has no reports, return empty list
- `lowest_common_manager(a, b)`
    - Return the lowest (deepest) `manager` that is an ancestor of both `a` and `b`
    - If one `employee` is the `manager` of the other, return that `manager`
    - If either `employee` doesn’t exist, return `None`

### Example


### Constraints


### Initial Thoughts, Questions
- `add_employee` equates to adding in a child to a manager
    - Child would have no direct employees at that time
    - Will CEO be added first? If there are existing people, and a new employee is added with `None` manager, I'd have to make assumption everyone without a parent will report into them
        - Eh assume CEO added before any employees ***that reference it***
        - If "add CEO" called again, raise error or ignore - for now we'll raise Error
    - Are there other semantics around adding in a new employee? If `manager` has 1 direct report already, and a new employee is added, the current assumption is both directly report up and there's no changing outside of that
- `get_reports` would be a DFS search downwards, order doesn't matter so we can go down each line
- `lca` algorithm for lowest common manager
    - There's no assumption employees exist, so need to be careful traversing and storing `self.resp` there
- Creation of a node class `class TreeNode(self, val, left, right)` as in typical LC problems will be easiest to work with
    - Store CEO as root once we get it
    - Any inserts and traversals would start from CEO for now
    - Therefore the only overall class storage is just `self.root` 
        - `self.root` would hold pointers to all other `TreeNode`
        - Connecting everyone once we get CEO will be annoying, ideally CEO comes first in `add_employee`
    - This was overengineering, and explicitly stated to remove and not include
        - Just use maps `children[manager]`, and `parent[employee]`
        - Store pointers to managers, so when a manager query comes in you can directly access it (i.e. just use dictionaries)
- Other questions
    - Should I add caching? no mention in spec, but queries being repeated and "reasonable efficiency" is vague
        - No caching atm
    - LCA API mentions potential missing employee, will the other 2 API's have any potential "bad queries", or can we assume they are all valid queries?
        - if manager doesn't exist in `get_reports` just return `[]`
    

### Implementation
```python
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
```