from action_layer import ActionLayer
from util import Pair
from proposition import Proposition
from proposition_layer import PropositionLayer


class PlanGraphLevel(object):
    """
    A class for representing a level in the plan graph.
    For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
    """
    independent_actions = set()  # updated to the independent_actions of the problem (graph_plan.py line 32)
    actions = []  # updated to the actions of the problem (graph_plan.py line 33 and planning_problem.py line 36)
    props = []  # updated to the propositions of the problem (graph_plan.py line 34 and planning_problem.py line 36)

    @staticmethod
    def set_independent_actions(independent_actions):
        PlanGraphLevel.independent_actions = independent_actions

    @staticmethod
    def set_actions(actions):
        PlanGraphLevel.actions = actions

    @staticmethod
    def set_props(props):
        PlanGraphLevel.props = props

    def __init__(self):
        """
        Constructor
        """
        self.action_layer = ActionLayer()  # see action_layer.py
        self.proposition_layer = PropositionLayer()  # see proposition_layer.py

    def get_proposition_layer(self):  # returns the proposition layer
        return self.proposition_layer

    def set_proposition_layer(self, prop_layer):  # sets the proposition layer
        self.proposition_layer = prop_layer

    def get_action_layer(self):  # returns the action layer
        return self.action_layer

    def set_action_layer(self, action_layer):  # sets the action layer
        self.action_layer = action_layer


    def isPreconditionsInPrevLayer(self,previous_proposition_layer,action):
        return previous_proposition_layer.all_preconds_in_layer(action)


    def isPropsInMutex(self,action,previous_proposition_layer):
        combs = []
        pre = action.get_pre()
        for con1 in pre:
            for con2 in pre:
                combs.append((con1,con2))
        
        # allCombs = list()
        # for preconds in combs:
        #     con1 , con2 = preconds
        #     if(con1 != con2):
        #         allCombs.append(preconds)
        
        allCombs = list(filter(lambda x : (x[0]!=x[1]) ,combs) )
        #now check if any of the pair props is in Mutex

        isInMutex = list(map(lambda conditions: (previous_proposition_layer.is_mutex(conditions[0],conditions[1])),allCombs))
        isNoMutex = not any(isInMutex)        
        return isNoMutex

    def update_action_layer(self, previous_proposition_layer):
        """
        Updates the action layer given the previous proposition layer (see proposition_layer.py)
        You should add an action to the layer if its preconditions are in the previous propositions layer,
        and the preconditions are not pairwise mutex.
        all_actions is the set of all the action (include noOp) in the domain
        You might want to use those functions:
        previous_proposition_layer.is_mutex(prop1, prop2) returns true
        if prop1 and prop2 are mutex at the previous propositions layer
        previous_proposition_layer.all_preconds_in_layer(action) returns true
        if all the preconditions of action are in the previous propositions layer
        self.actionLayer.addAction(action) adds action to the current action layer
        """
        all_actions = PlanGraphLevel.actions
        "*** YOUR CODE HERE ***"
        def addAct(action):
            return self.action_layer.add_action(action) 

        #applying add_action function for each action from filtered list which have its preconds in prev level
        #filtering only actions which their preconds are not pairwise mutex
        return list(map(lambda action : addAct(action),list(filter(lambda action :(self.isPropsInMutex(action,previous_proposition_layer)),
         list(filter(lambda action : (self.isPreconditionsInPrevLayer(previous_proposition_layer,action)),all_actions))))))

        # for action in all_actions:
        #     if (self.isPreconditionsInPrevLayer(previous_proposition_layer,action)
        #     and self.isPropsInMutex(action,previous_proposition_layer)):
        #         addAct(action)



    def update_mutex_actions(self, previous_layer_mutex_proposition):
        """
        Updates the mutex set in self.action_layer,
        given the mutex proposition from the previous layer.
        current_layer_actions are the actions in the current action layer
        You might want to use this function:
        self.actionLayer.add_mutex_actions(action1, action2)
        adds the pair (action1, action2) to the mutex set in the current action layer
        Note that an action is *not* mutex with itself
        """
        current_layer_actions = self.action_layer.get_actions()
        "*** YOUR CODE HERE ***"
        combs = []
        for ac1 in current_layer_actions:
            for ac2 in current_layer_actions:
                combs.append((ac1,ac2))

        def addMutexActs(pairOfActions):
            a1,a2 = pairOfActions
            return self.action_layer.add_mutex_actions(a1,a2) 

        return list(map(addMutexActs,list(filter(lambda x:mutex_actions(x[0],x[1],previous_layer_mutex_proposition),
        list(filter(lambda i: (i[0]!=i[1]),combs))))))


    def update_proposition_layer(self):
        """
        Updates the propositions in the current proposition layer,
        given the current action layer.
        don't forget to update the producers list!
        Note that same proposition in different layers might have different producers lists,
        hence you should create two different instances.
        current_layer_actions is the set of all the actions in the current layer.
        You might want to use those functions:
        dict() creates a new dictionary that might help to keep track on the propositions that you've
               already added to the layer
        self.proposition_layer.add_proposition(prop) adds the proposition prop to the current layer

        """
        current_layer_actions = self.action_layer.get_actions()
        "*** YOUR CODE HERE ***"
        for action in current_layer_actions:
            for prop in action.get_add():
                if prop not in self.proposition_layer.get_propositions():
                    self.proposition_layer.add_proposition(prop)
                prop.add_producer(action)

    def notInMutexPropositions(self,p1,p2):
        if Pair(p1,p2) in proposition_layer.mutexPropositions:
            return False
        return True

    def update_mutex_proposition(self):
        """
        updates the mutex propositions in the current proposition layer
        You might want to use those functions:
        mutex_propositions(prop1, prop2, current_layer_mutex_actions) returns true
        if prop1 and prop2 are mutex in the current layer
        self.proposition_layer.add_mutex_prop(prop1, prop2) adds the pair (prop1, prop2)
        to the mutex set of the current layer
        """
        current_layer_propositions = self.proposition_layer.get_propositions()
        current_layer_mutex_actions = self.action_layer.get_mutex_actions()
        "*** YOUR CODE HERE ***"
        combs = []
        for prop1 in current_layer_propositions:
            for prop2 in current_layer_propositions:
                combs.append((prop1,prop2))
        
        return list(map(lambda prop:self.proposition_layer.add_mutex_prop(prop[0],prop[1]),  # applying this function to each pair of props which are in same mutex
        list(filter(self.notInMutexPropositions,
        list(filter(lambda pr:(mutex_propositions(pr[0],pr[1],current_layer_mutex_actions)),
        list(filter(lambda pr: (pr[0]!= pr[1]),combs))))))))


    def expand(self, previous_layer):
        """
        Your algorithm should work as follows:
        First, given the propositions and the list of mutex propositions from the previous layer,
        set the actions in the action layer.
        Then, set the mutex action in the action layer.
        Finally, given all the actions in the current layer,
        set the propositions and their mutex relations in the proposition layer.
        """
        previous_proposition_layer = previous_layer.get_proposition_layer()
        previous_layer_mutex_proposition = previous_proposition_layer.get_mutex_props()

        "*** YOUR CODE HERE ***"
        self.update_action_layer(previous_proposition_layer)

        self.update_mutex_actions(previous_layer_mutex_proposition)

        self.update_proposition_layer()

        self.update_mutex_proposition()


    def expand_without_mutex(self, previous_layer):
        """
        Questions 11 and 12
        You don't have to use this function
        """
        previous_layer_proposition = previous_layer.get_proposition_layer()
        "*** YOUR CODE HERE ***"


def mutex_actions(a1, a2, mutex_props):
    """
    This function returns true if a1 and a2 are mutex actions.
    We first check whether a1 and a2 are in PlanGraphLevel.independent_actions,
    this is the list of all the independent pair of actions (according to your implementation in question 1).
    If not, we check whether a1 and a2 have competing needs
    """
    if Pair(a1, a2) not in PlanGraphLevel.independent_actions:
        return True
    return have_competing_needs(a1, a2, mutex_props)


def have_competing_needs(a1, a2, mutex_props):
    """
    Complete code for deciding whether actions a1 and a2 have competing needs,
    given the mutex proposition from previous level (list of pairs of propositions).
    Hint: for propositions p  and q, the command  "Pair(p, q) in mutex_props"
          returns true if p and q are mutex in the previous level
    """
    "*** YOUR CODE HERE ***"

    def isMutex(p,q):
        return Pair(p,q) in mutex_props
    precon1 = a1.get_pre()
    precon2 = a2.get_pre()

    for condition1 in precon1:
        for condition2 in precon2:
            if isMutex(condition1,condition2):
                return True
    return False







def mutex_propositions(prop1, prop2, mutex_actions_list):
    """
    complete code for deciding whether two propositions are mutex,
    given the mutex action from the current level (set of pairs of actions).
    Your update_mutex_proposition function should call this function
    You might want to use this function:
    prop1.get_producers() returns the set of all the possible actions in the layer that have prop1 on their add list
    """
    "*** YOUR CODE HERE ***"
    def isPairMutex(a1,a2):
        return (Pair(a1,a2) in mutex_actions_list)

    pro1 = prop1.get_producers()
    pro2 = prop2.get_producers()
    for ac1 in pro1:
        for ac2 in pro2:
            if(not isPairMutex(ac1,ac2)):
                return False
    return True

