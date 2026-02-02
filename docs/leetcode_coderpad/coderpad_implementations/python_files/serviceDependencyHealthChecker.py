from typing import Dict
from collections import defaultdict

class ServiceHealth():
    def __init__(self):
        self.service_dict: Dict[str, Dict] = {}
        # The services that each key needs to function
        self.service_to_depends_on = defaultdict(list)
        
        # Each service that's needed by key to function
        self.service_to_depended_by = defaultdict(list)
    
    def add_service(self, service: str) -> None:
        if service in self.service_dict.keys():
            raise ValueError(f"{service} already in dictionary")
                
        self.service_dict[service] = {
            "is_operational": False,
            "is_healthy": True,
        }
        return
    
    def add_dependency(self, service: str, depends_on: str) -> None:
        self.service_to_depends_on[service].append(depends_on)
        self.service_to_depended_by[depends_on].append(service)
        return None
    
    def set_unhealthy(self, service: str) -> None:
        # Sets the flg per service, doesn't compute the flag for all other dependent services

        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        
        self.service_dict[service]["is_healthy"] = False
        return None

    def set_healthy(self, service: str) -> None:
        # Sets the flg per service, doesn't compute the flag for all other dependent services

        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        
        self.service_dict[service]["is_healthy"] = True
        return None

    def is_operational(self, service: str) -> bool:
        if service not in self.service_dict.keys():
            raise ValueError(f"{service} not currently in dictionary")
        if self.service_dict[service]["is_healthy"] == False:
            return(False)
        
        has_cycle = False
        state = defaultdict(int)
        cache = defaultdict(int)
        
        
        def dfs(service: str):
            nonlocal has_cycle
            nonlocal state
            nonlocal cache

            count = 0
            
            if has_cycle:
                return(0)
            
            # If this doesn't exist, raise a ValueError
            if service not in self.service_dict.keys(): # or self.service_dict[service]["is_healthy"] == False:
                raise ValueError(f"{service} not currently in dictionary")
            
            # We will set cycle here
            if state[service] == 1:
                has_cycle = True
                return(0)
            # if this service has already been seen, we should still cover it
            elif state[service] == 2:
                return(cache[service])
            else:
                state[service] = 1
            
            
            # service_to_depends_on = {
            #     'a': [b, c],
            #     'b': [d, f],
            #     'c': [d],
            #     'd': [e]
            #     'e': []
            #     'f': []
            # }

            # D -> A
            
            # Because we're using `service_to_depends_on`, we're only touching the relevant
            #   subgraph, and has_cycle wouldn't be set on a cycle in a separate component
            for upstream_service in self.service_to_depends_on[service]:
                count += dfs(upstream_service)
            
            state[service] = 2
            cache[service] = (1 if count == len(self.service_to_depends_on[service]) else 0)
            # if all our dependent services are covered, then we're also covered
            return(
                1 if count == len(self.service_to_depends_on[service]) else 0
            )
            
        
                        