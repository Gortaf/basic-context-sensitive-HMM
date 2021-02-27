# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 01:00:30 2021

@author: Nicolas
"""

class Context_HMM:
    
    def __init__(self, data:str, splitter:str = '', blacklist:list = [], context_depth:int = 1):
        """
        A Hidden Markov Model with some form of context sensitiveness.
        Each next element decision is influenced by the ones that came before.
        The number of elements that will influence the next one is determined
        by the context depth

        Parameters
        ----------
        data : str
            The whole string from which to train to algorithm.
        splitter : str, optional
            The character that splits each elements.
            If nothing is specified every char is considered an element.
        blacklist : list, optional
            A list of elements to ignore when building the model.
        context_depth : int, optional
            The context depth to generate for each element. The default is 1.

        Returns
        -------
        None.

        """
        
        
        from tqdm import tqdm
        
        self.model = {}
        self.context_depth = context_depth
        
        # Splits the data
        if len(splitter) == 0:
            data = list(data)
            
        else:
            data = data.split(splitter)

        # Removes anything from the blacklist & empty sequences
        data = list(filter(lambda a: len(a) != 0 and a not in blacklist, data))
        
        # Adds "telomeres" to the list
        for i in range(context_depth):
                data = [""] + data
                data.append("")
        
        # Iterates through the data to generate the model
        for i,elem in enumerate(tqdm(data[:len(data)-context_depth])):
            
            # The slice of elements that come after w/ context_depth
            after = data[i+1:i+context_depth+1]
            
            # Creates a new entry if the element si unknown
            if elem not in self.model:
                # self.model[elem] = {}
                self.model[elem] = [{} for a in after]
            
            # Adds the element "after-context" to the existing entry
            # else:
            for i,a in enumerate(after):
                    if a in self.model[elem][i]:
                        self.model[elem][i][a] += 1
                    else:
                        self.model[elem][i][a] = 1
                    # self.model[elem][i].append(a)
            
            
            
    def get_next(self, element:str, context:list):
        """
        Returns an element that could follow the one passed, according to
        the context and the built model
        
        Parameters
        ----------
        element : str
            The element in the model from which to get a "next" element.
        context : list
            A list of the previous words. Max size should be same size as context_depth.

        Returns
        -------
        Type of HMM's elements
            The element that was choosen as the next one.

        """
        import random as rn
        choice_list = self.model[element][0]
        
        # for each context element, get their corresponding "after-context" list
        for i,elem in enumerate(context[::-1]):
            cor = self.model[elem][i]
            
            # Cross-compares compares context elements
            # then doubles their population on a match
            for a,ca in choice_list.items():
                for b,cb in cor.items():
                    if a==b:
                        choice_list[a] += cb
            
        
        rn_choice = []
        for elem,nb in choice_list.items():
            for i in range(nb):
                rn_choice.append(elem)
        return rn.choice(rn_choice)
        
    def generate(self, length:int, start = None, splitter:str = ''):
        """
        Generates a sequence based on the model

        Parameters
        ----------
        length : int
            The number of elements to put in the generated sequence.
        start : str, optional
            The element from which to start. If no elements are specified,
            then chooses a random one from the model
        splitter : str, optional
            Something to put between each element of the generated sequence. 

        Returns
        -------
        str
            the generated sequence.

        """
        from tqdm import tqdm
        
        # Gets a random start if none is specified
        if start == None:
            import random as rn
            start = rn.choice(list(self.model.keys()))
        
        out= [str(start)]
        
        # Generates the sequence by choosing a "next" element for each one
        # based on their context
        for i in tqdm(range(length)):
            ctx_i = i - self.context_depth
            if ctx_i < 0:
                ctx_i = 0
            
            start = self.get_next(start, out[ctx_i:i])
            out.append(str(start))
        
        return splitter.join(out)
    