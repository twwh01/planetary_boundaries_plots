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
    #   0 = baseline value
    #   1 = planetary boundary (edge of safe operating space)
    #   2 = upper limit of zone of increasing risk
    #   in the high-risk zone normalized values start at 2 and rise
    #       proportional to the width of the zone of increasing risk, i.e.
    #       for the functional diversity value: 
    #       boundary = 0.1, upper limit = 0.2, current value = 0.3
    #       the upper limit has been exceeded by 100% of the width of the zone
    #       of increasing risk so the normalized value is 2 + 1.00 = 3
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

        # a colour gradient function is used to create smooth transitions between colours
        # and to set the alpha (transparency) of each segment
        def gradient_color(start_color, end_color, steps, alpha=1.0):
            start_color = np.array(mcolors.to_rgba(start_color, alpha))
            end_color = np.array(mcolors.to_rgba(end_color, alpha))
            return [start_color * (1 - i / steps) + end_color * (i / steps) for i in range(steps)]

        # set the alpha value for each filled segment
        # # note that missing data are filled by solid grey with alpha=1
        seg_alpha = 0.75

        ax = plt.subplot(projection='polar')

        n_pb = self.size
        pbs = self.planetary_boundaries
        # width of each planetary boundary in the plot is determined by the number of boundaries
        width = ((2*np.pi) / n_pb) - (np.pi / (10*n_pb)) 
        # position of each planetary boundary in the plot
        theta = np.linspace(0, 2 * np.pi, n_pb, endpoint=False)
        n = 0
        t_manip = []

        # pre-compute the tallest bar across all quantified control variables so
        # the radial limit and the control-variable label ring can be sized from
        # the data before anything is drawn.
        H = 0
        for pb in pbs:
            for l in pb.limits:
                h = l.norm()
                if h is not None and not m.isnan(h):
                    H = max(H, h)
        # ring (radius) for the italic control-variable labels
        r_labels = max(H, 2) + 0.8

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
                
                none = 1
                t = t_list[rk]
                rk+=1

                # if height != None:
                if not m.isnan(height):
                    # safe operating space plotted as a solid green bar from 0 -> 1
                    # antialiased=False removes edge banding
                    ax.bar(t, min(height, 1), width=w,
                           facecolor=mcolors.to_rgba('green', seg_alpha),
                           edgecolor='none', antialiased=False, bottom=0)

                    # zone of increasing risk plotted as a yellow -> red gradient from 1 -> 2
                    # colour is mapped to the absolute radial position so that 1 is always yellow
                    # and 2 is always red with intermediate colours between 
                    if height > 1:
                        top = min(height, 2)
                        n_seg = 1000
                        seg_h = 1 / n_seg              # full zone width is 1 (r: 1 -> 2)
                        grad = gradient_color('yellow', 'red', n_seg, alpha=seg_alpha)
                        for i in range(n_seg):
                            r0 = 1 + i * seg_h         # inner radius of this segment
                            if r0 >= top:
                                break
                            # clip the final segment so the bar stops exactly at `top`
                            h = min(seg_h, top - r0)
                            ax.bar(t, h, width=w, facecolor=grad[i],
                                   edgecolor='none', antialiased=False,
                                   bottom=r0)

                    # high risk zone plotted as a red -> indigo gradient from 2 -> height
                    # the top is unconstrained as no upper boundary is defined for the high risk zone
                    if height > 2:
                        n_seg = 1000
                        seg_h = (height - 2) / n_seg
                        grad = gradient_color('red', 'indigo', n_seg, alpha=seg_alpha)
                        for i in range(n_seg):
                            ax.bar(t, seg_h, width=w, facecolor=grad[i],
                                   edgecolor='none', antialiased=False,
                                   bottom=2 + i * seg_h)

                    if control_var_label:
                        # add control variable labels to plot
                        control_var_text = re.sub('\\s', '\n', limit_name)
                        ax.annotate(control_var_text,
                                    xy = (t+(w/10), r_labels),
                                    ha='center', va='center',
                                    fontsize='xx-small', fontstyle='italic')
                    
                # if height == None:
                if m.isnan(height):
                    ax.bar(t, 1, width=w, color='grey', bottom=0)
                    
            if none == 0 :
                pb.name = pb.name + '\n(not yet quantified)'

        # add circle at r = 1 to indicate safe operating space
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        r_circle = np.full_like(theta_circle, 1)
        ax.plot(theta_circle, r_circle, color='green', linewidth=0.5, linestyle='--', zorder=10) 
        
        # add circle at r = 2 to indicate zone of increasing risk
        theta_circle = np.linspace(0, 2 * np.pi, 100)
        r_circle = np.full_like(theta_circle, 2)
        ax.plot(theta_circle, r_circle, color='red', linewidth=0.5, linestyle='--', zorder=10)

        # format the grid
        ax.grid(True, linewidth=0)
        angles = np.degrees(theta)
        ax.set_thetagrids(angles)

        # fixed radial extent so the rim is predictable
        # necessary to allow spaced plotting of the boundary and control variable labels
        # control-variable label ring at r_labels scaled by `resize`
        ax.set_ylim(0, (r_labels + 0.5) * resize)

        if label:
            ax.set_xticklabels(self.names(), fontweight='bold', fontsize='x-small')
            # push the planetary boundary labels outside the rim so they do not 
            # collide with the control variable labels
            ax.tick_params(axis='x', pad=20)
        else:
            ax.set_xticklabels([])

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