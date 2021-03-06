from multiprocessing.dummy import Array
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from scipy.stats import poisson
from scipy.stats import norm
import statistics
import seaborn as sns
from reliability.Distributions import Weibull_Distribution
import matplotlib.pyplot as plt


class Grapher:
    """
        Class for plotting diagrams for the simulation program
    """

    def build_histogram(data, title):
        """
            Takes an array of data and a title string, creates histogram
            
            Example call: Grapher.build_histogram([1,2,3,4,5], "Histogram")
        """
        # Calculating number of bins
        q25, q75 = np.percentile(data, [25, 75])
        bin_width = 2 * (q75 - q25) * len(data) ** (-1/3)
        bins = round((data.max() - data.min()) / bin_width)

        # Creating histogram
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.hist(data, bins=bins, ec='black')

        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()

    
    def build_qq_plot(list1, list2, title):
        """
            Takes two lists of data and plots them on the x and y axis respectively.
            
            Example call: Grapher.build_qq_plot([1,2,3,4,5], [1,2,3,4,5], "QQPlot")
        """
        plt.scatter(list1, list2)
        plt.axline([0, 0], [1, 1])
        # name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        # filename = '../output/figures/' + name
        plt.title(title)
        # plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        # plt.close()
        plt.show()

    def build_poission(lamb, title):
        """
            Takes an array of lambdas (can be 1 or more) and a title string, creates a plot
            with a poisson distribution for each lambda
            
            Example call: Grapher.build_poisson([5, 50, 25], "QQPlot")
            Example call: Grapher.build_poisson([5], "QQPlot")
        """
        legend = []
        x = np.arange(0, 100, 1)
        
        # Create and plot each poisson
        for i in range(len(lamb)):
            plt.plot(x, poisson.pmf(x, lamb[i]))
            legend.append("lambda = " + str(lamb[i]))
    
        plt.legend(legend)        

        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()


    def build_normal(mean, stddev, title):
        """
            Takes a mean, a standard deviation and a title string, creates a normal distribution plot
            
            Example call: Grapher.build_normal(3, 1, "Normal")
        """
        # Calculate range
        a = mean - (4 * stddev)
        b = mean + (4 * stddev)

        # Create normal plot
        x = np.arange(a, b, 0.01)
        plt.plot(x, norm.pdf(x, mean, stddev))

        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()

   
    def build_exponential(beta, title):
        """
            Takes an array of betas and a title string and creates a plot with an exponential distribution for each beta
            
            Example call: Grapher.build_exponential([5, 50, 25], "Exp")
            Example call: Grapher.build_exponential([5], "Exp")
        """
        legend = []
        size = 1000

        # Create and plot each exponential
        for i in range(len(beta)):
            sns.kdeplot(np.random.exponential(beta[i], size))
            legend.append("beta = " + str(beta[i]))

        plt.legend(legend)
        
        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()
    

    def build_weibull_costant_beta(alpha, title):
        """
            Takes an array of alphas and a title string and creates a plot with a Weibull distribution for each alpha 
            with a constant beta of 1. 
            
            Example call: Grapher.build_weibull_costant_beta([5, 50, 25], "Weibull")
            Example call: Grapher.build_weibull_costant_beta([5], "Weibull")
        """
        legend = []
        
        # Create and plot each weibull
        for i in range(len(alpha)):
            dist = Weibull_Distribution(alpha[i], 1)
            dist.PDF() 
            legend.append("beta = " + str(alpha[i]))

        plt.legend(legend)
        
        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()


    def build_weibull_double_param(alpha, beta, title):
        """
            Takes a single alpha and beta and a title string and plots a Weibull distribtuion 
            
            Example call: Grapher.build_weibull_double_param(5, 3, "Weibull2")
        """
        # Create the weibull plot
        dist = Weibull_Distribution(alpha, beta)
        dist.PDF() 

        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()


    def build_log_normal(mean, stddev, title):
        """
            Takes a mean, a standard deviation and a title string, creates a log normal distribution plot
            
            Example call: Grapher.build_log_normal(3, 1, "logNormal")
        """
        # Create and plot log normal 
        s = np.random.lognormal(mean, stddev, 1000)
        bins = plt.hist(s, 100, density=True, align='mid')
        x = np.linspace(min(bins), max(bins), 10000)
        pdf = (np.exp(-(np.log(x) - mean)**2 / (2 * stddev**2))
               / (x * stddev * np.sqrt(2 * np.pi)))

        plt.plot(x, pdf, linewidth=2, color='r')
        
        # Save plot to file
        name = title + '_' + date.today().strftime("%b-%d-%Y") + '_' + datetime.now().strftime("%H-%M-%S")
        filename = '../output/figures/' + name
        plt.title(name)
        plt.savefig(filename, dpi=200, bbox_inches="tight", facecolor="white")
        plt.close()


# Keep for testing
# np.random.seed(42)
# x = np.random.normal(size=1000)
# Grapher.build_histogram(x, "testHistogram")

