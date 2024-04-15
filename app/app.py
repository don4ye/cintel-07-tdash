import seaborn as sns  # Import seaborn for data visualization
from faicons import icon_svg  # Import icon_svg function from faicons module

from shiny import reactive  # Import reactive function from shiny module
from shiny.express import input, render, ui  # Import input, render, and ui functions from shiny.express module
import palmerpenguins  # Import palmerpenguins for dataset

# Load the penguins dataset
df = palmerpenguins.load_penguins()

# Set up the page options for the dashboard
ui.page_opts(title="Prince Ade's Penguins Dashboard", fillable=True)

# Create the sidebar with filter controls
with ui.sidebar(title="Filter controls"):
    # Input slider for selecting mass range
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    # Input checkbox group for selecting penguin species
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Add links to external resources
    ui.hr()  # Horizontal rule for separation
    ui.h6("Links")  # Heading for links section
    ui.a(
        "GitHub Source",  # Link text
        href="https://github.com/denisecase/cintel-07-tdash",  # Link URL
        target="_blank",  # Open link in new tab
    )
    ui.a(
        "GitHub App",
        href="https://github.com/don4ye/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/don4ye/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/don4ye/cintel-04-local",
        target="_blank",
    )

# Create layout for displaying penguin data
with ui.layout_column_wrap(fill=False):
    # Display number of penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]  # Return the number of rows in the filtered dataframe

    # Display average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"  # Return the mean bill length

    # Display average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"  # Return the mean bill depth

# Create layout for displaying plots and data tables
with ui.layout_columns():
    # Create a card for displaying scatterplot of bill length vs. bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            # Customize Seaborn's plotting style and color palette
            sns.set_style("whitegrid")  # Set the style of the plot
            sns.set_palette("pastel")  # Set the color palette

            # Plot the scatterplot with customized appearance
            scatterplot = sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
                palette="colorblind",  # Customize the color palette
                marker="o",  # Customize marker style
                s=100,  # Customize marker size
                alpha=0.8,  # Set transparency level
            )

            return scatterplot

    # Create a card for displaying summary statistics table
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]  # Columns to display in the table
            return render.DataGrid(filtered_df()[cols], filters=True)  # Display filtered dataframe in a data grid

# Define a reactive function to filter the dataframe based on user inputs
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]  # Filter dataframe by selected species
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]  # Filter dataframe by mass threshold
    return filt_df  # Return filtered dataframe
