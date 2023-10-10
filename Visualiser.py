import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



class RawVisualiser:

    def __init__(self, **params):
        self.params = params


    def plot_2d_scatter(self, samples, feature1: int, feature2: int):

        X = samples[0]
        y = samples[1]
        # Select the first two features for plotting
        x1 = X[:, feature1]
        x2 = X[:, feature2]

        # Create a DataFrame for plotting
        df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'Class': y})

        # Map class labels to more descriptive names
        class_labels = {0: 'Majority Class', 1: 'Minority Class'}
        df['Class'] = df['Class'].map(class_labels)

        # Create the scatter plot using Plotly
        fig = px.scatter(
            df,
            x='Feature 1',
            y='Feature 2',
            color='Class',
            marginal_x= "histogram", 
            marginal_y= "histogram",
            title='2D Scatter Plot of Imbalanced Data',
            labels={'Feature 1': f'Feature {feature1}', 'Feature 2': f'Feature {feature2}'}
        )

        fig.show()
        #return fig
    

    def plot_2d_scatter_multiple_datasets_go(self, 
                                             datasets, 
                                             feature1=0, 
                                             feature2=1,
                                             feature_map = {},
                                             title="2D Scatter Plot", 
                                             color_sequence=None,
                                             save = False):
        """
        Create a 2D scatter plot for multiple datasets.

        Args:
            datasets (list of tuple): List of tuples, where each tuple contains a dataset (X, y) and a label.
            feature1 (int): Index of the first feature to plot (default is 0).
            feature2 (int): Index of the second feature to plot (default is 1).
            title (str): Title of the plot (default is "2D Scatter Plot").
            color_sequence (list): List of colors for dataset labels (default is None,
                                which uses Plotly's default color sequence).

        Returns:
            None (displays the plot).
        """

        # Create the scatter plot using Plotly
        if color_sequence is None:
            color_sequence = px.colors.qualitative.Plotly

        # Create a color mapping dictionary to ensure class colors are consistent within datasets
        color_mapping = {}
        dataset_color_index = 0

        fig = go.Figure()

        for i, (X, y, label) in enumerate(datasets):

            if label not in color_mapping:
                color_mapping[label] = dataset_color_index
                dataset_color_index += 1

            class_colors = [color_sequence[(color_mapping[label] + i) % len(color_sequence)] for i in range(len(np.unique(y)))]
            #print(class_colors)
            
            # Select the two features for plotting
            x1 = X[:, feature1]
            x2 = X[:, feature2]

            # Map class labels to more descriptive names
            class_labels = {val: f'{label} - Class {int(val)}' for val in np.unique(y)}

            df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'Class': y})
            df['Class'] = df['Class'].map(class_labels)

            for j, class_val in enumerate(np.unique(y)):
                data = df[df['Class'] == f'{label} - Class {int(class_val)}']
                fig.add_trace(go.Scatter(
                    x=data['Feature 1'],
                    y=data['Feature 2'],
                    mode='markers',
                    name=f'{label} - Class {int(class_val)}',
                    marker=dict(
                        size=8,
                        opacity=0.7,
                        color = class_colors[j],
                    )
                ))

        x_title = feature_map.get(feature1, f'Feature {feature1 + 1}')
        y_title = feature_map.get(feature2, f'Feature {feature2 + 1}')

        fig.update_layout(
            title=title,
            xaxis_title=f'Feature {feature1}',
            yaxis_title=f'Feature {feature2}',
            legend=dict(x=0.85, y=1.0),
        )

        if save:
            fig.write_image(f"Figures/{title}.png")

        fig.show()



    def plot_2d_scatter_multiple_datasets_px(self, 
                                             datasets, 
                                             feature1=0, 
                                             feature2=1,
                                             feature_map = {},
                                             title="2D Scatter Plot",
                                             save = False):
        """
        Create a 2D scatter plot for multiple datasets.

        Args:
            datasets (list of tuple): List of tuples, where each tuple contains a dataset (X, y) and a label.
            feature1 (int): Index of the first feature to plot (default is 0).
            feature2 (int): Index of the second feature to plot (default is 1).
            title (str): Title of the plot (default is "2D Scatter Plot").

        Returns:
            None (displays the plot).
        """
        df = pd.DataFrame()

        for (X, y, label) in datasets:
            
            # Select the two features for plotting
            x1 = X[:, feature1]
            x2 = X[:, feature2]

            # Map class labels to more descriptive names
            class_labels = {val: f'{label} - Class {int(val)}' for val in np.unique(y)}

            set_df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'Class': y})
            set_df['Class'] = set_df['Class'].map(class_labels)

            df = pd.concat([df, set_df])

        #print(df)
        fig = px.scatter(
            df,
            x = 'Feature 1',
            y = 'Feature 2',
            color = 'Class',
            marginal_x= "histogram", 
            marginal_y= "histogram",
        )

        x_title = feature_map.get(feature1, f'Feature {feature1 + 1}')
        y_title = feature_map.get(feature2, f'Feature {feature2 + 1}')

        fig.update_layout(
            title = title,
            xaxis_title = x_title,
            yaxis_title = y_title,
            legend = dict(x=0.85, y=1.0),
        )

        title = title.replace(" ", "_")
        if save:
            fig.write_image(f"Figures/{title}.png", 
                            width=1920, 
                            height=1080, 
                            scale=3
                            )

        fig.show()



    def plot_3d_scatter_multiple_datasets_px(self, datasets, feature1=0, feature2=1, feature3 =2, title="3D Scatter Plot"):


        df = pd.DataFrame()

        for (X, y, label) in datasets:
            
            # Select the two features for plotting
            x1 = X[:, feature1]
            x2 = X[:, feature2]
            x3 = X[:, feature3]

            # Map class labels to more descriptive names
            class_labels = {val: f'{label} - Class {int(val)}' for val in np.unique(y)}

            set_df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'Feature 3': x3, 'Class': y})
            set_df['Class'] = set_df['Class'].map(class_labels)

            df = pd.concat([df, set_df])


        fig = px.scatter_3d(
            df,
            x = 'Feature 1',
            y = 'Feature 2',
            z = 'Feature 3',
            color='Class',
            #size = 5* np.ones(len(X)),
            size_max = 15,
            opacity = 0.9,
            width = 1400,
            height = 1000,
            #margin = dict(b=50),
            #title='3D Scatter Plot of Imbalanced Data',
            #labels={'Feature 1': f'Feature {feature_x}', 'Feature 2': f'Feature {feature_y}', 'Feature 3': f'Feature {feature_z}'}
        )

        fig.update_layout(
            title=title,
            scene = dict(
            xaxis_title=f'Feature {feature1}',
            yaxis_title=f'Feature {feature2}',
            zaxis_title=f'Feature {feature3}',
            ),
            legend=dict(x=0.85, y=1.0),
        )

        fig.show()



    def plot_3d_scatter_multi_class(self, class_data_dict, class_labels):
        """
        Plot samples from multiple classes in a 3D scatter plot.

        Args:
            class_data_dict (dict): A dictionary where keys are class labels and values are 3D data arrays.
            class_labels (list): A list of class labels in the order they should appear in the legend.

        Example:
            class_data_dict = {
                'Class A': np.random.rand(30, 3),
                'Class B': np.random.rand(30, 3),
                'Class C': np.random.rand(30, 3)
            }
            class_labels = ['Class A', 'Class B', 'Class C']
        """

        traces = []

        for label, data in zip(class_labels, class_data_dict.values()):
            trace = go.Scatter3d(
                x=data[:, 0],
                y=data[:, 1],
                z=data[:, 2],
                mode='markers',
                name=label,
                marker=dict(
                    size=5,
                    opacity=0.7,
                )
            )
            traces.append(trace)

        layout = go.Layout(
            title='3D Scatter Plot for Multiple Classes',
            scene=dict(
                xaxis_title='X Axis',
                yaxis_title='Y Axis',
                zaxis_title='Z Axis',
            ),
        )

        fig = go.Figure(data=traces, layout=layout)
        fig.show()








class CLSFVisualiser:

    def __init__(self, **params):
        self.params = params


    def confusion_scatterplot(self, 
                              X_test,
                              y_test,
                              y_predicted, 
                              feature1=0, 
                              feature2=1,
                              feature_map = {},
                              title="Confusion Scatterplot",
                              save = False):
        
        y_test_1_mask = y_test == 1
        y_pred_1_mask = y_predicted == 1

        confusion_dict = {
            'True Negatives': X_test[(~y_test_1_mask) & (~y_pred_1_mask), :],
            'False Positives': X_test[(~y_test_1_mask) & (y_pred_1_mask), :],
            'True Positives': X_test[(y_test_1_mask) & (y_pred_1_mask), :],
            'False Negatives': X_test[(y_test_1_mask) & (~y_pred_1_mask), :],
        }

        df = pd.DataFrame()

        for label, X_data in confusion_dict.items():
            # Select the two features for plotting
            x1 = X_data[:, feature1]
            x2 = X_data[:, feature2]

            group_df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'Label': label})

            df = pd.concat([df, group_df])
        #print(df)

        color_dict = {
            'True Positives': 'green',
            'False Negatives': 'red',
            'False Positives': 'purple',
            'True Negatives': px.colors.qualitative.Safe[0],
        }

        fig = px.scatter(
            df,
            x = 'Feature 1',
            y = 'Feature 2',
            color = 'Label',
            color_discrete_map = color_dict,
            marginal_x= "histogram", 
            marginal_y= "histogram",
        )

        #fig.update_traces(marker=dict(color='red'))

        x_title = feature_map.get(feature1, f'Feature {feature1 + 1}')
        y_title = feature_map.get(feature2, f'Feature {feature2 + 1}')

        fig.update_layout(
            title = title,
            xaxis_title = x_title,
            yaxis_title = y_title,
            legend = dict(x=0.85, y=1.0),
        )

        title = title.replace(" ", "_")
        if save:
            fig.write_image(f"Figures/{title}.png", 
                            width=1920, 
                            height=1080, 
                            scale=3
                            )

        fig.show()


    
    def pred_proba_scatterplot(self, 
                               X_test,
                               predicted_proba,
                               corr_classes, 
                               feature1=0, 
                               feature2=1,
                               feature_map = {},
                               title="Probability Scatterplot",
                               save = False):
        
        pred_proba = predicted_proba[:, np.where(corr_classes == 1)[0]].flatten()

        df = pd.DataFrame()

        # Select the two features for plotting
        x1 = X_test[:, feature1]
        x2 = X_test[:, feature2]

        df = pd.DataFrame({'Feature 1': x1, 'Feature 2': x2, 'C1 Probability': pred_proba})

        fig = px.scatter(
            df,
            x = 'Feature 1',
            y = 'Feature 2',
            color = 'C1 Probability',
            #color_continuous_scale = 'Bluered',
            #color_continuous_scale=["blue", "green", "red"],
            color_continuous_scale = 'OrRd',
            #color_continuous_scale = 'Plasma_r',
        )

        x_title = feature_map.get(feature1, f'Feature {feature1 + 1}')
        y_title = feature_map.get(feature2, f'Feature {feature2 + 1}')

        fig.update_layout(
            title = title,
            xaxis_title = x_title,
            yaxis_title = y_title,
            legend = dict(x=0.85, y=1.0),
        )

        title = title.replace(" ", "_")
        if save:
            fig.write_image(f"Figures/{title}.png", 
                            width=1920, 
                            height=1080, 
                            scale=3
                            )

        fig.show()



   


    




if __name__ == "__main__":

    import scipy.stats as st
    from Data_Generator import Multi_Modal_Dist_Generator
    

    """
    Visualise
    -------------------------------------------------------------------------------------------------------------------------------------------
    
    dist_gen_spec = Multi_Modal_Dist_Generator(distributions, dist_parameter_dicts, size)


    dist_gen_spec.create_data()
    spec_samples = (dist_gen_spec.X, dist_gen_spec.y)
    #spec_samples = dist_gen_spec.prepare_data(0.2)

    visualiser = RawVisualiser()

    visualiser.plot_2d_scatter(spec_samples, 0, n-1)
    visualiser.plot_3d_scatter(spec_samples, 0, 1, 2)
    """


    """
    Plotly Experiments
    -------------------------------------------------------------------------------------------------------------------------------------------
    """
    df = px.data.iris()
    #print(df)
    fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", symbol="species")
    
    fig.show()

    gapminder = px.data.gapminder()
    gapminder2=gapminder.copy(deep=True)
    gapminder['planet']='earth'
    gapminder2['planet']='mars'
    gapminder3=pd.concat([gapminder, gapminder2])

    fig = px.bar(gapminder3, x="continent", y="pop", color="planet",
    animation_frame="year", animation_group="country", range_y=[0,4000000000*2])
    #fig.show()