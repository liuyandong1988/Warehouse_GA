# -*- coding: utf-8 -*-

import random
from Life import Life

class GA(object):
    """遗传算法类"""
    def __init__(self, cross_rate, mutation_rate, population_size, init_chromosome, chromosome_length, fitness_Fun = lambda life : 1):
        self.cross_rate = cross_rate               #the probability of crossover
        self.mutation_rate = mutation_rate         #the probability of mutation
        self.population_size = population_size               #the number of the population
        self.init_chromosome = init_chromosome 
        self.chromosome_length = chromosome_length         #the length of the chromosome
        self.fitness_Fun = fitness_Fun                 #the fitness function
        self.population = []                          
        self.best = None                          #the best chromosome
        self.generation = 1                       #generation
        self.cross_cnt = 0                      
        self.mutation_cnt = 0                    
        self.bounds = 0.0                         #the sum of the fitness
        self.initPopulation()                   
    
    
    def initPopulation(self):
        """initial the population"""
        self.population = []
        for i in range(self.population_size):
            #gene = [0,1,…… ,self.chromosome_length-1]
            gene = self.init_chromosome[:]
            random.shuffle(gene)
            pop = Life(gene)
            # put individual in the population
            self.population.append(pop)
#         print self.population[0].gene 
#         print self.population[15].gene 
#         print self.population[50].gene 
#         raw_input('prompt')
    
    def judgeChromosome(self):
        """judge the individual fitness"""
        # the sum of fitness
        self.bounds = 0.0
        self.best = self.population[0]
        for chromosome in self.population:
            chromosome.score = self.fitness_Fun(chromosome)
            self.bounds += chromosome.score
            if self.best.score < chromosome.score:
                self.best = chromosome
    
    
    def cross(self, parent1, parent2):
        """crossover"""
        index1 = random.randint(0, self.chromosome_length - 1)
        index2 = random.randint(index1, self.chromosome_length - 1)
        tempGene = parent2.gene[index1:index2]                  
        new_gene = []
        p1_len = 0
        for g in parent1.gene:
            if p1_len == index1:
                new_gene.extend(tempGene)                             
                p1_len += 1
            if g not in tempGene:
                new_gene.append(g)
                p1_len += 1
        self.cross_cnt += 1
        return new_gene
    
    
    def  mutation(self, gene):
        """mutation"""
        index1 = random.randint(0, self.chromosome_length - 1)
        index2 = random.randint(0, self.chromosome_length - 1)
        #exchange the city position
        gene[index1], gene[index2] = gene[index2], gene[index1]
        self.mutation_cnt += 1
        return gene
    
    
    def getOne(self):
        """choose a chromosome"""
        r = random.uniform(0, self.bounds)
        for popu in self.population:
            r -= popu.score
            if r <= 0:
                return popu
        raise Exception("Error!!!", self.bounds)
    
    
    def newChromosome(self):
        """generate the new chromosome"""
        parent1 = self.getOne()
        rate = random.random()
        # crossover
        if rate < self.cross_rate:
            # crossover
            parent2 = self.getOne()
            chromosome = self.cross(parent1, parent2)
        else:
            chromosome = parent1.gene
        #mutation
        rate = random.random()
        if rate < self.mutation_rate:
            chromosome = self.mutation(chromosome)
        return Life(chromosome)
    
    
    def nextGeneration(self):
        """the next generation """
        self.judgeChromosome()  # judge the individual fitness
        new_population = []
        new_population.append(self.best) # add the best child
        while len(new_population) < self.population_size:
            new_population.append(self.newChromosome())
        self.population = new_population
        self.generation += 1
