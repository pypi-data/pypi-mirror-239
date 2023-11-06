#%%
from numpy import pi

class AngularFrequency():
    """Angular Frequency object
    """    
    def __init__(self, w):
        self.w = w
    
    @classmethod
    def from_rpm(cls, rpm:float):
        """Create an AngularFrequency object from rpm (Factory class method)

        Args:
            rpm (float): revolutions per minute

        Returns:
            AngularFrequency: _description_
        """        
        return cls(2*pi/60 *rpm)


    @classmethod
    def from_r_wn(cls, r:float, wn:float):
        """Factory class method 

        Args:
            r ([float]): ratio of frequencies
            wn ([float]): eigenfrequency

        Returns:
            [float]: frequency
        """        
        return cls(r*wn)


# %%
