from machine import Pin, time_pulse_us
import utime

from machine import Pin, time_pulse_us
import utime

class HCSR04() :
    ''' A l'instanciation, donnez les numéros des broches en paramètres sur lesquelles sont connectées Trig et Echo 
    La méthode distance renvoie la distance en mm sinon -1 lorsque la mesure n'a pas aboutie
    La méthode n_mesures renvoie la moyenne de  n mesures  de la distnace en mm ( n passé en paramètres) 
    '''
    
    def __init__(self,broche_trig,broche_echo):
       self.Pin_trig = broche_trig
       self.Pin_echo = broche_echo

    def distance(self):   
        sig = Pin(self.Pin_trig, Pin.OUT)
        sig.value(0)  
        sig.value(1) #déclenchement du trigger >10us  mesuré 33us
        utime.sleep_us(10)
        sig.value(0)
        sig = Pin(self.Pin_echo, Pin.IN)
        t = time_pulse_us(sig, 1, 24000) # timeout pour 4m  = 2 * 11700
        dist_mm = 340000 * t // 2000000  
        utime.sleep_ms(60) #temps mini entre 2 mesures  (60ms)
        return dist_mm
    
    def n_mesures(self, n) : #moyenne sur n mesures
        somme = 0
        for i in range (n) :
            dist = self.distance()
            somme = somme + dist
        moyenne = somme // n
        return moyenne


class HCSR04_GROVE() :
    ''' Sur groove : SIG correspond à Trig et Echo donc broche_trig = broche_echo = broche_SIG
    A l'instanciation, donnez le numéro de la broche connectée en paramètre sur laquelle est  connectée SIG 
    La méthode distance renvoie la distance en mm sinon -1 lorsque la mesure n'a pas aboutie
    La méthode n_mesures renvoie la moyenne de  n mesures  de la distnace en mm ( n passé en paramètres) 
    '''
    def __init__(self,broche_SIG):
        self.broche = broche_SIG
    
    def distance(self):   
        sig = Pin(self.broche, Pin.OUT)
        sig.value(0)
        #utime.sleep_us(5)
        sig.value(1)
        utime.sleep_us(10)
        sig.value(0)
        sig = Pin(self.broche, Pin.IN)
        t = time_pulse_us(sig, 1, 24000) # timeout pour 4m  = 2 * 11700
        dist = 340000 * t // 2000000
        utime.sleep_ms(60) #temps mini entre 2 mesures  (60ms)
        return dist_mm
   
    def n_mesures(self, n) : #moyenne sur n mesures
        somme = 0
        for i in range (n) :
            dist = self.distance()
            somme = somme + dist
        moyenne = somme // n
        return moyenne
    
if __name__ == '__main__':
    #instanciation d’un objet
    capteur_HCSR_1 = HCSR04_GROVE(1)

    while True:
        #mesure = HCSR04_GROVE(1).distance()   
        #print(mesure)
        mesure = HCSR04_GROVE(1).n_mesures(10)   
        print(mesure)
        utime.sleep_ms(200)