import matplotlib.pyplot as plt
import numpy as np
import os
from typing import Union, List, Dict, Optional, Tuple


def plot_line(data: Union[List, Dict, Tuple],
              x_data: Optional[Union[List, np.ndarray]] = None,
              xlabel: str = "X Axis",
              ylabel: str = "Y Axis",
              title: str = "Line Plot",
              legend: Optional[Union[List[str], bool]] = None,
              save_path: Optional[str] = None,
              figsize: Tuple[int, int] = (10, 6),
              style: str = 'default',
              grid: bool = True,
              **kwargs):
    """
    Convenient function to create line plots

    Parameters:
    -----------
    data : Union[List, Dict, Tuple]
        Data, supports multiple formats:
        - List: single data series [1, 2, 3, 4]
        - Dict: multiple data series {"series1": [1,2,3], "series2": [2,3,4]}
        - Tuple: (x_data, y_data) or (x_data, {"series1": y1, "series2": y2})

    x_data : Optional[Union[List, np.ndarray]]
        X-axis data, if not provided, indices will be used

    xlabel : str
        X-axis label

    ylabel : str  
        Y-axis label

    title : str
        Chart title

    legend : Optional[Union[List[str], bool]]
        Legend settings:
        - None: automatically decide whether to display legend
        - List[str]: custom legend labels
        - bool: True to show, False to hide

    save_path : Optional[str]
        Save path, supports relative and absolute paths

    figsize : Tuple[int, int]
        Figure size (width, height)

    style : str
        matplotlib style

    grid : bool
        Whether to display grid

    **kwargs : 
        Additional parameters passed to plt.plot()
    """

    # Set style
    plt.style.use(style)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Process data format
    if isinstance(data, dict):
        # Multiple data series: {"series1": [1,2,3], "series2": [2,3,4]}
        series_names = list(data.keys())

        for i, (name, y_values) in enumerate(data.items()):
            if x_data is not None:
                ax.plot(x_data, y_values, label=name, **kwargs)
            else:
                ax.plot(y_values, label=name, **kwargs)

    elif isinstance(data, (list, tuple)) and len(data) == 2 and isinstance(data[1], dict):
        # Format: (x_data, {"series1": y1, "series2": y2})
        x_vals, y_dict = data
        series_names = list(y_dict.keys())

        for name, y_values in y_dict.items():
            ax.plot(x_vals, y_values, label=name, **kwargs)

    elif isinstance(data, (list, tuple)) and len(data) == 2 and not isinstance(data[1], dict):
        # Format: (x_data, y_data) single data series
        x_vals, y_vals = data
        ax.plot(x_vals, y_vals, **kwargs)
        series_names = None
        
    elif isinstance(data, (list, tuple)) and all(isinstance(item, (list, tuple)) for item in data):
        if x_data is None:
            x_data = list(range(len(data[0])))
        
        for i, y_values in enumerate(data):
            plt.plot(x_data, y_values, label=f'Series {i+1}')
        
        plt.legend()
        series_names = None

    else:
        # Single data series: [1, 2, 3, 4]
        if x_data is not None:
            ax.plot(x_data, data, **kwargs)
        else:
            ax.plot(data, **kwargs)
        series_names = None

    # Set labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Handle legend
    if legend is True or (legend is None and series_names is not None):
        if isinstance(legend, list):
            ax.legend(legend)
        else:
            ax.legend()
    elif isinstance(legend, list):
        ax.legend(legend)

    # Grid
    if grid:
        ax.grid(True, alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Save image
    if save_path:
        # Ensure directory exists
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Image saved to: {save_path}")

    plt.show()
    return fig, ax

def plot_bar(data: Union[List, Dict, Tuple],
             x_data: Optional[Union[List, np.ndarray]] = None,
             xlabel: str = "X Axis",
             ylabel: str = "Y Axis", 
             title: str = "Bar Plot",
             legend: Optional[Union[List[str], bool]] = None,
             save_path: Optional[str] = None,
             figsize: Tuple[int, int] = (10, 6),
             style: str = 'default',
             grid: bool = True,
             bar_type: str = 'grouped',  # 'grouped' or 'stacked'
             width: float = 0.8,
             **kwargs):
    """
    Convenient function to create bar plots

    Parameters:
    -----------
    data : Union[List, Dict, Tuple]
        Data, supports multiple formats:
        - List: single data series [1, 2, 3, 4]
        - Dict: multiple data series {"series1": [1,2,3], "series2": [2,3,4]}
        - Tuple: (x_data, y_data) or (x_data, {"series1": y1, "series2": y2})

    x_data : Optional[Union[List, np.ndarray]]
        X-axis labels/positions, if not provided, indices will be used

    xlabel : str
        X-axis label

    ylabel : str  
        Y-axis label

    title : str
        Chart title

    legend : Optional[Union[List[str], bool]]
        Legend settings:
        - None: automatically decide whether to display legend
        - List[str]: custom legend labels
        - bool: True to show, False to hide

    save_path : Optional[str]
        Save path, supports relative and absolute paths

    figsize : Tuple[int, int]
        Figure size (width, height)

    style : str
        matplotlib style

    grid : bool
        Whether to display grid

    bar_type : str
        Bar chart type: 'grouped' or 'stacked'

    width : float
        Bar width (0.0 to 1.0)

    **kwargs : 
        Additional parameters passed to plt.bar()
    """

    # Set style
    plt.style.use(style)

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Process data format
    if isinstance(data, dict):
        # Multiple data series: {"series1": [1,2,3], "series2": [2,3,4]}
        series_names = list(data.keys())
        series_data = list(data.values())
        
        if x_data is None:
            x_data = list(range(len(series_data[0])))
        
        x_pos = np.arange(len(x_data))
        
        if bar_type == 'stacked':
            # Stacked bar chart
            bottom = np.zeros(len(x_data))
            for i, (name, y_values) in enumerate(data.items()):
                ax.bar(x_pos, y_values, width, label=name, bottom=bottom, **kwargs)
                bottom += np.array(y_values)
        else:
            # Grouped bar chart
            bar_width = width / len(series_names)
            for i, (name, y_values) in enumerate(data.items()):
                offset = (i - len(series_names)/2 + 0.5) * bar_width
                ax.bar(x_pos + offset, y_values, bar_width, label=name, **kwargs)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_data)

    elif isinstance(data, (list, tuple)) and len(data) == 2 and isinstance(data[1], dict):
        # Format: (x_data, {"series1": y1, "series2": y2})
        x_vals, y_dict = data
        series_names = list(y_dict.keys())
        
        x_pos = np.arange(len(x_vals))
        
        if bar_type == 'stacked':
            # Stacked bar chart
            bottom = np.zeros(len(x_vals))
            for name, y_values in y_dict.items():
                ax.bar(x_pos, y_values, width, label=name, bottom=bottom, **kwargs)
                bottom += np.array(y_values)
        else:
            # Grouped bar chart
            bar_width = width / len(series_names)
            for i, (name, y_values) in enumerate(y_dict.items()):
                offset = (i - len(series_names)/2 + 0.5) * bar_width
                ax.bar(x_pos + offset, y_values, bar_width, label=name, **kwargs)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_vals)

    elif isinstance(data, (list, tuple)) and len(data) == 2 and not isinstance(data[1], dict):
        # Format: (x_data, y_data) single data series
        x_vals, y_vals = data
        x_pos = np.arange(len(x_vals))
        ax.bar(x_pos, y_vals, width, **kwargs)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_vals)
        series_names = None
        
    elif isinstance(data, (list, tuple)) and all(isinstance(item, (list, tuple)) for item in data):
        # Multiple data series as list of lists
        series_names = [f'Series {i+1}' for i in range(len(data))]
        
        if x_data is None:
            x_data = list(range(len(data[0])))
        
        x_pos = np.arange(len(x_data))
        
        if bar_type == 'stacked':
            # Stacked bar chart
            bottom = np.zeros(len(x_data))
            for i, y_values in enumerate(data):
                ax.bar(x_pos, y_values, width, label=series_names[i], bottom=bottom, **kwargs)
                bottom += np.array(y_values)
        else:
            # Grouped bar chart
            bar_width = width / len(data)
            for i, y_values in enumerate(data):
                offset = (i - len(data)/2 + 0.5) * bar_width
                ax.bar(x_pos + offset, y_values, bar_width, label=series_names[i], **kwargs)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_data)

    else:
        # Single data series: [1, 2, 3, 4]
        if x_data is None:
            x_data = list(range(len(data)))
        
        x_pos = np.arange(len(x_data))
        ax.bar(x_pos, data, width, **kwargs)
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_data)
        series_names = None

    # Set labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Handle legend
    if legend is True or (legend is None and series_names is not None):
        if isinstance(legend, list):
            ax.legend(legend)
        else:
            ax.legend()
    elif isinstance(legend, list):
        ax.legend(legend)

    # Grid
    if grid:
        ax.grid(True, alpha=0.3, axis='y')  # Only show horizontal grid for bar charts

    # Adjust layout
    plt.tight_layout()

    # Save image
    if save_path:
        # Ensure directory exists
        dir_path = os.path.dirname(save_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Image saved to: {save_path}")

    plt.show()
    return fig, ax


def main():
    a = 0   # empty operation

if __name__ == "__main__":
    main()
