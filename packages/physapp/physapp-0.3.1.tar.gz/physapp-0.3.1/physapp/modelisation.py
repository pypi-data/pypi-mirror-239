import numpy as np

import matplotlib.pyplot as plt
from matplotlib.legend import Legend
from matplotlib.lines import Line2D

import scipy.stats as sstats
from scipy.optimize import curve_fit

from physapp.utils import pround, reduire
from physapp.fonctions import *



class Modele():

    _id = 0
    _loc = 3

    def __init__(self, xy_data, function, xlim, popt, pcov, infos_dic):
        
        

        self._xdata, self._ydata = xy_data  # x, y (Numpy array) des données à l'origine du modèle
        self._function = function           # Fonction ajustement
        self._popt = popt                   # paramètres optimales obtenus
        self._pcov = pcov                   # covariance des paramètres
        self._perr = None                   # incertitudes-type élargies sur les paramètres


        self._modele_name = infos_dic['modele_name']
        self._modele_shortname = infos_dic['modele_shortname']         
        self._expression_text = infos_dic['expression_text']  
        self._expression_latex = infos_dic['expression_latex']
        self._popt_names_text = infos_dic['popt_names_text']
        self._popt_names_latex = infos_dic['popt_names_latex']
        self._xlogspace = infos_dic['xlogspace']

        Modele._id = (Modele._id + 1)%10
        self._name =  self._modele_shortname + " (" + str(self._id) + ")"

        self._niv_confiance = 0.95          # niveau de confiance pour coeff. de Student
        self._nb_round = 3                  # nombre de chiffres significatifs

        self._x = None                      # tableau Numpy x de la courbe du modèle
        self._y = None                      # tableau Numpy y de la courbe du modèle
        self._xmin = xlim[0]                # limite inférieure xmin pour le tracé de la courbe du modèle
        self._xmax = xlim[1]                # limite supérieure xmax pour le tracé de la courbe du modèle
        self._nb_pts = 200                  # nombre de points pour le tracé de la courbe du modèle
        self._line2D = None

        self._legend = None
        self._legend_str = ""               # texte de l'étiquette de la courbe du modèle
        Modele._loc +=1
        self._legend_loc = self._loc

        
        self.__update_perr()
        self.__update_legend()
        self.__update_xy()

    
    def __popt_latex(self):
        names = self._popt_names_latex
        values = self.popt()
        errors = self.perr() 
        str = ''
        
        for i in range(len(values)):
            str = str + names[i] + r"$=$" + "(" + pround(values[i], self._nb_round) + r"$~\pm$" + pround(errors[i],2) + ")\n"
        return str[:-1]
        
    def __popt_text(self):
        names = self._popt_names_text
        values = self.popt()
        errors = self.perr()
        str = ''
        for i in range(len(values)):
            str = str + names[i] + "=" + "(" + pround(values[i], self._nb_round) + " \xb1" + pround(errors[i],2) + ")\n"
        return str[:-1]

    def __update_legend(self):
        #name = self._modele_name
        expression = self._expression_latex
        resultats = self.__popt_latex()
        confiance = "Niv. confiance de " + str(int(self._niv_confiance*100)) + "%"
        self._legend_str =  expression + '\n' + resultats + '\n' + confiance
    
    def __update_perr(self):
        u = np.sqrt(np.diag(self._pcov))                    # incertitudes-type  = variance des paramètres (diagonale)
        n, p = len(self._xdata), len(self._popt)            # Nombre de points - Nombre de paramètres
        ts = sstats.t.ppf(1-(1-self._niv_confiance)/2, n-p) # Coeff. de Student
        self._perr = ts*u                                   # incertitudes-type élargies
        
    def __update_xy(self):
        if self._xlogspace == True:
            self._x = np.logspace(np.log10(self._xmin), np.log10(self._xmax), self._nb_pts)
            self._y = self._function(self._x, *self._popt)
        else:
            self._x = np.linspace(self._xmin, self._xmax, self._nb_pts)
            self._y = self._function(self._x, *self._popt)
     
    def get_id(self):
        return self._id
    
    def get_xmin(self):
        """ Renvoie xmin pour le tracé de la courbe du modèle.

        Renvoie :
            (float) : borne inférieure
        """
        return self._xmin

    def set_xmin(self, xmin):
        """ Modifie xmax pour le tracé de la courbe du modèle.

        Paramètres :
            xmin (float) : borne inférieure
        """
        if xmin < self._xmax:
            self._xmin = xmin
            self.__update_xy()
        
    def get_xmax(self):
        """ Renvoie la borne supérieure de x pour le tracé de la courbe du modèle.

        Renvoie :
            xmax (float) : borne supérieure
        """
        return self._xmax
        
    def set_xmax(self, xmax):
        """ Modifie la borne supérieure de x pour le tracé de la courbe du modèle.

        Paramètres :
            xmax (float) : borne supérieure
        """
        if xmax > self._xmin:
            self._xmax = xmax
            self.__update_xy()
            
    def get_nb_pts(self):
        """ Renvoie le nombre de points pour  le tracé de la courbe du modèle.

        Renvoie :
            (int) : nombre de points
        """
        return self._nb_pts
        
    def set_nb_pts(self, nb_pts: int):
        """ Modifie le nombre de points pour le tracé de la courbe du modèle.

        Paramètres :
            nb_pts (int) : nombre de points
        """
        self._nb_pts = nb_pts
        self.__update_xy()

    def get_nb_round(self):
        """ Renvoie le nombre de chiffres significatifs pour l'affichage des valeurs.

        Renvoie :
            (int) : nombre de chiffres significatifs
        """
        return self._nb_round
    
    def set_nb_round(self, nb: int):
        """ Modifie le nombre de chiffres significatifs pour l'affichage des valeurs.

        Paramètres :
            nb_round (float) : nombre de chiffres significatifs
        """
        self._nb_round = nb
        self.__update_legend()

    
    def get_niveau_confiance(self):
        """ Renvoie la valeur du niveau de confiance entre 0 et 1.

        Renvoie :
            (float)
        """
        return self._niv_confiance
    
    def set_niveau_confiance(self, niv:float):
        """ Modifie la valeur du niveau de confiance entre 0 et 1.

        Paramètres :
            niv (float) : entre 0 et 1
        """
        if 0<niv<1:
            self._niv_confiance = niv
            self.__update_legend()
        else:
            raise ValueError("Le niveau de confiance doit-être strictement compris entre 0 et 1 !")

    def popt(self):
        """ Renvoie les paramètres optimales obtenus pour le modèle.

        Renvoie :
            popt (Numpy array)
        """
        return self._popt
    
    def pcov(self):
        """ Renvoie les covariances des paramètres du modèle.
        
        Renvoie :
            pcov (Numpy array)
        """
        return self._pcov
    
    def perr(self):
        """ Renvoie les incertitudes-type élargies des paramètres du modèle.

        Renvoie :
        .perr (Numpy array)
        """
        
        return self._perr
    
    def get_xy(self):
        """ Renvoie les données x et y de la courbe du modèle.
        
        Renvoie :
            x, y (Numpy array)
        """
        return self._x, self._y
    
    
   
    def __str__(self):
        """ Affiche le résultat détaillé de la modélisation.

        Renvoie :
            (str)
        """
        fonction = self._modele_name
        expression = self._expression_text
        resultats = self.__popt_text()
        confiance = "Avec un intervalle de confiance de " + str(int(self._niv_confiance*100)) + "% sans incertitudes sur x et y."
        return fonction + '\n' + expression + '\n' + resultats + '\n' + confiance


    def plot(self, *args, **kargs) -> Line2D:
        """ Trace la courbe y=f(x) du modèle dans le repère (matplotlib.pyplot.axes) en cours.

        Paramètres :
            *args (matplotlib.line.line2D)
            **kargs (matplotlib.line.line2D)
        
        Renvoie :
            ligne (matplotlib.pyplot.line2D)
        """
        default_kargs = {
            "label":self._name
        }
        for key in kargs.keys():               # Supprime les options par défaut si en argument
            if key in default_kargs.keys():
                del default_kargs[key]

        ax = plt.gca()
        line = ax.plot(self._x, self._y, *args, **kargs, **default_kargs)
        self._line2D = line[0]

        return self._line2D




    def legend(self, *args, **kargs) -> Legend:
        """"
        """       
        default_kargs = {
            'loc':self._legend_loc,
            'draggable':True,
            'title':self._name,
            'title_fontproperties':{'weight':'bold'},
            'fancybox': True,
            'framealpha': 0.8,
            'handlelength': 0,
            'handletextpad': 0,
            'draggable': True,
            'facecolor': "white"   
        }
        for key in kargs.keys():              # Supprime les options par défaut si en argument
            if key in default_kargs.keys():
                del default_kargs[key]

        ax = plt.gca()
        if self._line2D != None:
            self._legend = Legend(ax, [self._line2D], [self._legend_str], *args, **kargs, **default_kargs)
            ax.add_artist(self._legend)

        return self._legend
    




    
###########################################################
#              FONCTIONS CLASSIQUES                       #
###########################################################
    
# Ajustement suivant une fonction linéaire
def ajustement_lineaire(x, y, x_inf: float = None, x_sup: float = None, a0: float = 1):
    
    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(lineaire, x, y, p0=[a0])  
    infos_dic = {
        'modele_name'     : 'Fonction linéaire',
        'modele_shortname': 'Fonction linéaire',
        'expression_text' : 'y = a*x',
        'expression_latex': r"$y=a\cdot x$",
        'popt_names_text' : ['a'],
        'popt_names_latex': ['$a$'],
        'xlogspace'       : False
        }
    return Modele((x,y),lineaire, xlim, popt, pcov, infos_dic)


# Ajustement suivant une fonction affine
def ajustement_affine(x, y, x_inf: float = None, x_sup: float = None, a0: float = 1, b0: float = 1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(affine, x, y, p0=[a0, b0])
    infos_dic = {
        'modele_name'     : 'Fonction affine',
        'modele_shortname': 'Fonction affine',
        'expression_text' : 'y = a*x + b',
        'expression_latex': r'$y=a\cdot x + b$',
        'popt_names_text' : ['a', 'b'],
        'popt_names_latex': ['$a$', '$b$'],
        'xlogspace'       : False
        }
    return Modele((x,y), affine, xlim, popt, pcov, infos_dic)



# Ajustement suivant une fonction parabolique
def ajustement_parabolique(x, y, x_inf: float = None, x_sup: float = None, a0: float = 1, b0: float = 1, c0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(parabole, x, y, p0=[a0, b0, c0])
    infos_dic = {
        'modele_name'     : 'Fonction parabolique',
        'modele_shortname': 'Fonction parabolique',
        'expression_text' : 'y = a*x^2 + b*x + c',
        'expression_latex': r"$y=a\cdot x^2+b\cdot x+c$",
        'popt_names_text' : ['a', 'b', 'c'],
        'popt_names_latex': ['$a$', '$b$', '$c$'],
        'xlogspace'       : False
        }
    return Modele((x,y),parabole, xlim, popt, pcov, infos_dic)




# Ajustement suivant une fonction exponentielle croissante
def ajustement_exponentielle_croissante(x, y, x_inf: float = None, x_sup: float = None, A0: float = 1, tau0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(exponentielle_croissante, x, y, p0=[A0, tau0])
    infos_dic = {
        'modele_name'     : 'Fonction exponentielle croissante',
        'modele_shortname': 'Fonction exponentielle',
        'expression_text' : 'y = A*(1-exp(-x/tau))',
        'expression_latex': r'$y=A\cdot(1-e^{-x/\tau})$',
        'popt_names_text' : ['A', 'tau'],
        'popt_names_latex': ['$A$', r'$\tau$'],
        'xlogspace'       : False
        }
    return Modele((x,y),exponentielle_croissante, xlim, popt, pcov, infos_dic)


def ajustement_exponentielle_decroissante(x, y, x_inf: float = None, x_sup: float = None, A0: float = 1, tau0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(exponentielle_decroissante, x, y, p0=[A0, tau0])
    infos_dic = {
        'modele_name'     : 'Fonction exponentielle décroissante',
        'modele_shortname': 'Fonction exponentielle',
        'expression_text' : 'y = A*exp(-x/tau)',
        'expression_latex': r'$y=A\cdot e^{-x/\tau}$',
        'popt_names_text' : ['A', 'tau'],
        'popt_names_latex': ['$A$', r'$\tau$'],
        'xlogspace'       : False
        }
    return Modele(exponentielle_decroissante, xlim, popt, pcov, infos_dic)


def ajustement_exponentielle2_croissante(x, y, x_inf: float = None, x_sup: float = None, A0: float = 1, k0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(exponentielle2_croissante, x, y, p0=[A0, k0])
    infos_dic = {
        'modele_name'     : 'Fonction exponentielle croissante',
        'modele_shortname': 'Fonction exponentielle',
        'expression_text' : 'y = A*(1-exp(-k*x))',
        'expression_latex': r'$y=A\cdot(1-e^{-k\cdot x})$',
        'popt_names_text' : ['A', 'k'],
        'popt_names_latex': ['$A$', '$k$'],
        'xlogspace'       : False
        }
    return Modele((x,y),exponentielle2_croissante, xlim, popt, pcov, infos_dic)


def ajustement_exponentielle2_decroissante(x, y, x_inf: float = None, x_sup: float = None, A0: float = 1, k0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(exponentielle2_decroissante, x, y, p0=[A0, k0])
    infos_dic = {
        'modele_name'     : 'Fonction exponentielle décroissante',
        'modele_shortname': 'Fonction exponentielle',
        'expression_text' : 'y = A*exp(-k*x)',
        'expression_latex': r'$y=A\cdot e^{-k\cdot x}$',
        'popt_names_text' : ['A', 'k'],
        'popt_names_latex': ['$A$', '$k$'],
        'xlogspace'       : False
        }
    return Modele((x,y),exponentielle2_decroissante, xlim, popt, pcov, infos_dic)



def ajustement_puissance(x, y, x_inf: float = None, x_sup: float = None, A0: float = 1, n0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(puissance, x, y, p0=[A0, n0])
    infos_dic = {
        'modele_name'     : 'Fonction puissance',
        'modele_shortname': 'Fonction puissance',
        'expression_text' : 'y = A*x^n',
        'expression_latex': r'$y=A\cdot x^n$',
        'popt_names_text' : ['A', 'n'],
        'popt_names_latex': ['$A$', '$n$'],
        'xlogspace'       : False
        }
    return Modele((x,y),puissance, xlim, popt, pcov, infos_dic)


###########################################################
#              REPONSE ORDRE 1  - PASSE BAS               #
###########################################################
def ajustement_ordre1_passe_bas_transmittance(x, y, x_inf: float = None, x_sup: float = None, T0=1, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_bas_transmittance, x, y, p0=[T0, f0])
    infos_dic = {
        'modele_name'     : "Transmittance - Passe bas d'ordre 1",
        'modele_shortname': "Transmittance",
        'expression_text' : 'T = T0/sqrt(1+(f/f0)^2)',
        'expression_latex': r"$T = \dfrac{T_0}{\sqrt{1+(\dfrac{f}{f_0})^2}}$",
        'popt_names_text' : ['T0', 'f0'],
        'popt_names_latex': ['$T_0$', '$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_bas_transmittance, xlim, popt, pcov, infos_dic)


def ajustement_ordre1_passe_bas_gain(x, y, x_inf: float = None, x_sup: float = None, G0=0, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_bas_gain, x, y, p0=[G0, f0])
    infos_dic = {
        'modele_name'     : "Gain - Passe bas d'ordre 1",
        'modele_shortname': "Gain",
        'expression_text' : 'G = G0 - 20*log(sqrt(1+(f/f0)^2))',
        'expression_latex': r"$G = G_0 - 20\cdot\log(\sqrt{1+(\dfrac{f}{f_0})^2})$",
        'popt_names_text' : ['G0', 'f0'],
        'popt_names_latex': ['$G_0$', '$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_bas_gain, xlim, popt, pcov, infos_dic)



def ajustement_ordre1_passe_bas_dephasage(x, y, x_inf: float = None, x_sup: float = None, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_bas_dephasage, x, y, p0=[f0])
    infos_dic = {
        'modele_name'     : "Déphasage - Passe bas d'ordre 1",
        'modele_shortname': "Déphasage",
        'expression_text' : 'phi = -arctan(f/f0)',
        'expression_latex': r"$\varphi = -\arctan(\dfrac{f}{f_0})$",
        'popt_names_text' : ['f0'],
        'popt_names_latex': ['$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_bas_dephasage, xlim, popt, pcov, infos_dic)


###########################################################
#              REPONSE ORDRE 1  - PASSE HAUT              #
###########################################################

def ajustement_ordre1_passe_haut_transmittance(x, y, x_inf: float = None, x_sup: float = None, T0=1, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_haut_transmittance, x, y, p0=[T0, f0])
    infos_dic = {
        'modele_name'     : "Transmittance - Passe haut d'ordre 1",
        'modele_shortname': "Transmittance",
        'expression_text' : 'T = T0*(f/f0)/sqrt(1+(f/f0)^2)',
        'expression_latex': r"$T = \dfrac{T_0\cdot\dfrac{f}{f_0}}{\sqrt{1+(\dfrac{f}{f_0})^2}}$",
        'popt_names_text' : ['T0', 'f0'],
        'popt_names_latex': ['$T_0$', '$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_haut_transmittance, xlim, popt, pcov, infos_dic)


def ajustement_ordre1_passe_haut_gain(x, y, x_inf: float = None, x_sup: float = None, G0=0, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_haut_gain, x, y, p0=[G0, f0])
    infos_dic = {
        'modele_name'     : "Gain - Passe haut d'ordre 1",
        'modele_shortname': "Gain",
        'expression_text' : 'G = G0 + 20*log(f/f0) - 20*log(sqrt(1+(f/f0)^2))',
        'expression_latex': r"$G = G_0 + 20\cdot\log(\dfrac{f}{f_0})- 20\cdot\log(\sqrt{1+(\dfrac{f}{f_0})^2})$",
        'popt_names_text' : ['G0', 'f0'],
        'popt_names_latex': ['$G_0$', '$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_haut_gain, xlim, popt, pcov, infos_dic)



def ajustement_ordre1_passe_haut_dephasage(x, y, x_inf: float = None, x_sup: float = None, f0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre1_passe_haut_dephasage, x, y, p0=[f0])
    infos_dic = {
        'modele_name'     : "Déphasage - Passe haut d'ordre 1",
        'modele_shortname': "Déphasage",
        'expression_text' : 'phi = 90 - arctan(f/f0)',
        'expression_latex': r"$\varphi = 90 -\arctan(\dfrac{f}{f_0})$",
        'popt_names_text' : ['f0'],
        'popt_names_latex': ['$f_0$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre1_passe_haut_dephasage, xlim, popt, pcov, infos_dic)



###########################################################
#              REPONSE ORDRE 2  - PASSE BAS               #
###########################################################
def ajustement_ordre2_passe_bas_transmittance(x, y, x_inf: float = None, x_sup: float = None, T0=1, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bas_transmittance, x, y, p0=[T0, f0, m0])
    infos_dic = {
        'modele_name'     : "Transmittance - Passe bas d'ordre 2",
        'modele_shortname': "Transmittance",
        'expression_text' : "T = T0/sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2)",
        'expression_latex': r"$T = \dfrac{T_0}{\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2}}$",
        'popt_names_text' : ['T0', 'f0', 'm'],
        'popt_names_latex': ['$T_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bas_transmittance, xlim, popt, pcov, infos_dic)


def ajustement_ordre2_passe_bas_gain(x, y, x_inf: float = None, x_sup: float = None, G0=0, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bas_gain, x, y, p0=[G0, f0, m0])
    infos_dic = {
        'modele_name'     : "Gain - Passe bas d'ordre 2",
        'modele_shortname': "Gain",
        'expression_text' : 'G = G0 + 20*log((f/f0)^2) - 20*log(sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2))',
        'expression_latex': r"$G = G_0 - 20\cdot\log(\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2})$",
        'popt_names_text' : ['G0', 'f0', 'm'],
        'popt_names_latex': ['$G_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bas_gain, xlim, popt, pcov, infos_dic)



def ajustement_ordre2_passe_bas_dephasage(x, y, x_inf: float = None, x_sup: float = None, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bas_dephasage, x, y, p0=[f0, m0])
    infos_dic = {
        'modele_name'     : "Déphasage - Passe bas d'ordre 2",
        'modele_shortname': "Déphasage",
        'expression_text' : 'phi = 180 - arctan((2*m*f/f0)/(1-(f/f0)^2))',
        'expression_latex': r"$\varphi = -\arctan(\dfrac{2m\dfrac{f}{f_0}}{1-\dfrac{f^2}{f_0^2}})$",
        'popt_names_text' : ['f0', 'm'],
        'popt_names_latex': ['$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bas_dephasage, xlim, popt, pcov, infos_dic)


###########################################################
#              REPONSE ORDRE 2  - PASSE HAUT              #
###########################################################
def ajustement_ordre2_passe_haut_transmittance(x, y, x_inf: float = None, x_sup: float = None, T0=1, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_haut_transmittance, x, y, p0=[T0, f0, m0])
    infos_dic = {
        'modele_name'     : "Transmittance - Passe haut d'ordre 2",
        'modele_shortname': "Transmittance",
        'expression_text' : "T = T0*(f/f0)^2/sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2)",
        'expression_latex': r"$T = \dfrac{T_0\cdot\dfrac{f^2}{f_0^2}}{\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2}}$",
        'popt_names_text' : ['T0', 'f0', 'm'],
        'popt_names_latex': ['$T_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_haut_transmittance, xlim, popt, pcov, infos_dic)


def ajustement_ordre2_passe_haut_gain(x, y, x_inf: float = None, x_sup: float = None, G0=0, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_haut_gain, x, y, p0=[G0, f0, m0])
    infos_dic = {
        'modele_name'     : "Gain - Passe haut d'ordre 2",
        'modele_shortname': "Gain",
        'expression_text' : 'G = G0 + 20*log((f/f0)^2) - 20*log(sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2))',
        'expression_latex': r"$G = G_0 + 20\cdot\log(\dfrac{f^2}{f_0^2})- 20\cdot\log(\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2})$",
        'popt_names_text' : ['G0', 'f0', 'm'],
        'popt_names_latex': ['$G_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_haut_gain, xlim, popt, pcov, infos_dic)



def ajustement_ordre2_passe_haut_dephasage(x, y, x_inf: float = None, x_sup: float = None, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_haut_dephasage, x, y, p0=[f0, m0])
    infos_dic = {
        'modele_name'     : "Déphasage - Passe haut d'ordre 2",
        'modele_shortname': "Déphasage",
        'expression_text' : 'phi = 180 - arctan((2*m*f/f0)/(1-(f/f0)^2))',
        'expression_latex': r"$\varphi = 180 -\arctan(\dfrac{2m\dfrac{f}{f_0}}{1-\dfrac{f^2}{f_0^2}})$",
        'popt_names_text' : ['f0', 'm'],
        'popt_names_latex': ['$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_haut_dephasage, xlim, popt, pcov, infos_dic)


###########################################################
#              REPONSE ORDRE 2  - PASSE BANDE             #
###########################################################
def ajustement_ordre2_passe_bande_transmittance(x, y, x_inf: float = None, x_sup: float = None, T0=1, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bande_transmittance, x, y, p0=[T0, f0, m0])
    infos_dic = {
        'modele_name'     : "Transmittance - Passe bande d'ordre 2",
        'modele_shortname': "Transmittance",
        'expression_text' : "T = T0*2*m*(f/f0)/sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2)",
        'expression_latex': r"$T = T_0\cdot\dfrac{2m\cdot\dfrac{f}{f_0}}{\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2}}$",
        'popt_names_text' : ['T0', 'f0', 'm'],
        'popt_names_latex': ['$T_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bande_transmittance, xlim, popt, pcov, infos_dic)


def ajustement_ordre2_passe_bande_gain(x, y, x_inf: float = None, x_sup: float = None, G0=0, f0=1, m0=1):

    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bande_gain, x, y, p0=[G0, f0, m0])
    infos_dic = {
        'modele_name'     : "Gain - Passe bande d'ordre 2",
        'modele_shortname': "Gain",
        'expression_text' : 'G = G0 + 20*log(2*m*f/f0) - 20*log(sqrt((1-(f/f0)^2)^2+(2*m*f/f0)^2))',
        'expression_latex': r"$G = G_0 + 20\cdot\log(2m\dfrac{f}{f_0})- 20\cdot\log(\sqrt{(1-\dfrac{f^2}{f_0^2})^2+(2m\dfrac{f}{f_0})^2})$",
        'popt_names_text' : ['G0', 'f0', 'm'],
        'popt_names_latex': ['$G_0$', '$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bande_gain, xlim, popt, pcov, infos_dic)



def ajustement_ordre2_passe_bande_dephasage(x, y, x_inf: float = None, x_sup: float = None, f0=1, m0=1):
    # Problème décalage pour f=f0
    x, y, xlim = reduire(x, y, x_inf, x_sup)
    popt, pcov  = curve_fit(ordre2_passe_bande_dephasage, x, y, p0=[f0, m0])
    infos_dic = {
        'modele_name'     : "Déphasage - Passe bande d'ordre 2",
        'modele_shortname': "Déphasage",
        'expression_text' : 'phi = 90 - arctan((2*m*f/f0)/(1-(f/f0)^2)) [-180 si f>f0]',
        'expression_latex': r"$\varphi = 90 -\arctan(\dfrac{2m\dfrac{f}{f_0}}{1-\dfrac{f^2}{f_0^2}}) [-180~si~f>f_0]$",
        'popt_names_text' : ['f0', 'm'],
        'popt_names_latex': ['$f_0$', '$m$'],
        'plot_label_type' : 'name',
        'xlogspace'       : True 
        }
    return Modele((x,y),ordre2_passe_bande_dephasage, xlim, popt, pcov, infos_dic)