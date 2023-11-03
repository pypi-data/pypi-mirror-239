class Fact:
    
    def result(self,n):
        fact=1
        for i in range(n,0,-1):
            fact=fact*i
        return fact

        
    