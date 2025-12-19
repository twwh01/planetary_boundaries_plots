# define the planetary boundary class
class ControlVariable:
    """
    Attributes:
        name                str     name of the Limit object
        current_value       float   current value of the planetary boundary variable
        baseline_value      float   baseline value of the planetary boundary variable
        boundary_value      float   planetary boundary limit value
        upper_value         float   planetary boundary upper end of zone of increasing risk value
    """
    
    def __init__(self, name: str, current_value: float, baseline_value: float, boundary_value: float, upper_value: float, max=None, min=None):
        self.name = name
        self.baseline_value = baseline_value
        self.current_value = current_value
        self.boundary_value = boundary_value
        self.upper_value = upper_value
        self.max = max
        self.min = min
    
    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}('{self.name}', {self.current_value}, {self.baseline_value}, {self.boundary_value}, {self.upper_value})"
            
    # this section calculates control variable values normalised for their 
    # respective baseline, boundary, and upper limit values as follows:
    #   a value of 0 = baseline value
    #   a value of 1 = planetary boundary
    #   a value of 2 = upper limit of zone of increasing risk
    #   in the high-risk zone normalized values start at 2 and rise
    #       proportional to the width of the zone of increasing risk, i.e.
    #       for the functional diversity value: 
    #       boundary = 0.1, upper limit = 0.2, current value = 0.3
    #       the upper limit has been exceeded by 100% of the width of the zone
    #       of increasing risk so the normalized value is 2 + 1.0 = 3
    def __normal(self, current_value: float, baseline_value: float, boundary_value: float, upper_value: float) -> float:
        if current_value == None:
            return None
        else:
            width_of_safe_zone = abs(boundary_value - baseline_value)
            width_of_risk_zone = abs(upper_value - boundary_value)
        
            if boundary_value > baseline_value: # lower values are safer
                if current_value > upper_value: # exceeding zone of increasing risk
                    impact = 2 + ((current_value - upper_value) / width_of_risk_zone)
                
                elif current_value > boundary_value: # within zone of increasing risk
                    impact = 1 + ((current_value - baseline_value) / width_of_risk_zone)
                
                else: # within safe zone
                    impact = (current_value - baseline_value) / width_of_safe_zone
                
            else: # higher values are safer
                if current_value < upper_value: # exceeding zone of increasing risk
                    impact = 2 + ((upper_value - current_value) / width_of_risk_zone)
                
                elif current_value < boundary_value: # within zone of increasing risk
                    impact = 1 + ((boundary_value - current_value) / width_of_risk_zone)
                
                else:
                    impact = (baseline_value - current_value) / width_of_safe_zone
            
            return impact
    
    def norm(self) -> float:
        return self.__normal(self.current_value, self.baseline_value, self.boundary_value, self.upper_value)

    # def norm_max(self) -> float:
    #     return self.__normal(self.max, self.boundary_value, self.upper_value)
    
    # def norm_min(self) -> float:
    #     return self.__normal(self.min, self.boundary_value, self.upper_value)
        
    # def norm_upper_risk(self) -> float:
    #     return self.__init__(self.boundary_value, self.upper_value)


class PlanetaryBoundary:
    """
    Attributes:
        name                str     name of the PlanetaryBoundary object
        limits              list    list of control variables from ControlVariable class
    """
    def __init__(self, name: str, limits: list[ControlVariable]):
        self.name = name
        self.limits = limits
        self.size = len(limits)

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}('{self.name}', {self.limits})"

    def names(self) -> list[str]:
        names = []
        for l in self.limits :
            names.append(l.name)
        return names


class PlanetarySystem:
    """
    Attributes:
        name                    str     name of the PlanetarySystem object
        planetary_boundaries    list    list of planetary boundaries from the PlanetaryBoundary classs        
    """
    def __init__(self, name: str, planetary_boundaries: list[PlanetaryBoundary]):
        self.name = name
        self.planetary_boundaries = planetary_boundaries
        self.size = len(planetary_boundaries)

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}('{self.name}', {self.planetary_boundaries})"

    def names(self) -> list[str]:
        names = []
        for pb in self.planetary_boundaries :
                names.append(pb.name)
        return names

    def plot(self, label=True, control_var_label=True, resize=1) :
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.colors as mcolors
        import math as m
        import re

        # colour gradient function
        def gradient_color(start_color, end_color, steps):
            start_color = np.array(mcolors.to_rgba(start_color))
            end_color = np.array(mcolors.to_rgba(end_color))
            return [start_color * (1 - i / steps) + end_color * (i / steps) for i in range(steps)]

        ax = plt.subplot(projection='polar')

        n_pb = self.size
        pbs = self.planetary_boundaries
        # width of each planetary boundary in the plot is determined by the number of boundaries
        width = ((2*np.pi) / n_pb) - (np.pi / (10*n_pb)) 
        # position of each planetary boundary in the plot
        theta = np.linspace(0, 2 * np.pi, n_pb, endpoint=False)
        n = 0
        t_manip = []
        H = 0
        
        for pb in pbs:
            nb_cat = pb.size # number of planetary boundary control variables
            w = width / nb_cat # width of each control variable in the plot
            t_start = theta[n] - (((nb_cat-1)*w) / 2)
            n += 1

            t_list = list(np.linspace(t_start, t_start + (nb_cat-1)*w, nb_cat))

            if nb_cat > 1:
                t_manip += list(np.linspace(t_start + w/2, t_start + (nb_cat-1)*w + w/2, nb_cat-1, endpoint=False))

            rk = 0
            none = 0

            for l in pb.limits:
                limit_name = l.name
                print(limit_name)
                height = l.norm()
                
                # moved from inside if statement
                none = 1
                num_segments = 10000
                segment_height = height / num_segments
                t = t_list[rk]
                rk+=1
                
                # if height != None:
                if not m.isnan(height):
                    colors = []

                    for i in range(num_segments):
                        # set segment radius
                        current_height = i * segment_height
                        if current_height <= 1:
                            # while current value is within safe operating space 
                            # set colour to green
                            colors.append(mcolors.to_rgba('green'))
                        elif current_height <= 2:
                            # while current value is in zone of increasing risk
                            # set a yellow-red colour gradient
                            gradient_pos = (current_height - 1)# / (height - 1)
                            colors.append(gradient_color('yellow', 'red', 100)[int(gradient_pos * 99)])
                        else:
                            # while current value is in high risk zone
                            # set a red-purple colour gradient
                            gradient_pos = (current_height - 2) / (height - 2)
                            colors.append(gradient_color('red', 'indigo', 100)[int(gradient_pos * 99)])
                    
                    # add segments to plot
                    for i in range(num_segments):
                        ax.bar(t, segment_height, width=w, facecolor=colors[i], edgecolor='none', bottom=i * segment_height)
                    
                    if control_var_label:
                        # add control variable labels to plot
                        # ax.annotate(limit_name, xy = (t+(w/2), 6), ha='center', va='center')
                        control_var_text = re.sub('\\s', '\n', limit_name)
                        ax.annotate(control_var_text, 
                                    xy = (t+(w/10), 6), 
                                    ha='center', va='center', 
                                    fontsize='xx-small', fontstyle='italic')
                    
                # if height == None:
                if m.isnan(height):
                    ax.bar(t, 1, width=w, color='grey', bottom=0)
                    
            if none == 0 :
                pb.name = pb.name + '\n(not yet quantified)'

        # safe operating space
        # add circle at r = 1 to indicate safe operating space
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        r_circle = np.full_like(theta_circle, 1)
        ax.plot(theta_circle, r_circle, color='green', linewidth=0.5, linestyle='--') 
        
        # zone of increasing risk
        ## add circle at r = 2 to indicate zone of increasing risk
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        r_circle = np.full_like(theta_circle, 2)
        ax.plot(theta_circle, r_circle, color='red', linewidth=0.5, linestyle='--') 


        # format the grid
        ax.grid(True, linewidth=0)
        angles = np.degrees(theta)
        ax.set_thetagrids(angles)
        
        if label:
            ax.set_xticklabels(self.names(), fontweight='bold', fontsize='x-small')
        else:
            ax.set_xticklabels([])
        
        # ax.set_ylim(top=max(m.floor(H)+1,2)*resize+1)

        # add boundary separation lines
        theta2 = list(np.linspace(np.pi/n_pb, 2 * np.pi + np.pi/n_pb, n_pb, endpoint=False))
        for angle in theta2:
            ax.axvline(x=angle, color='grey', linestyle='-', linewidth=1)

        for angle in t_manip :
            ax.axvline(x=angle, color='grey', linestyle='-', linewidth=0.5, alpha=0.25)

        # remove rose diagram circles
        ax.spines['polar'].set_visible(False)

        # remove y-axis labels and grid
        ax.set_yticklabels([])

        return ax