# Italy Fuel Price Dashboard

This project is a data visualization dashboard designed to provide Italian citizens with a comprehensive overview of fuel prices across the country. It aims to offer transparency and historical context regarding the costs of Benzina (Petrol) and Gasolio (Diesel).

## Dataset

The dataset used in this application is generated using the [fuel-price-Italy-dataset-generator](https://github.com/MarcoBidoli/fuel-price-Italy-dataset-generator). It aggregates open data from the *Ministero delle Imprese e del Made in Italy (MIMIT)* to provide regional and temporal insights.

## Project Goal

The primary objective is to empower citizens with easy-to-digest information about fuel price trends, regional differences, and the impact of global events on local costs. The dashboard is structured to show data by importance:

1.  **Absolute Price (KPIs)**: Immediate view of the current average prices for major fuel types.
2.  **Regional Price Map**: A choropleth map showing the distribution of absolute prices across Italian regions.
3.  **Regional Deviation Map (%)**: A specialized map highlighting how each region deviates from the national average, providing a clear comparison of relative costs.
4.  **Price Evolution (Line Chart)**: A historical view of price changes over time, including markers for significant geopolitical and economic events.

## Technologies Used

The dashboard is built using a modern Python-based data stack:

*   **[Dash](https://dash.plotly.com/)**: A productive Python framework for building web analytic applications.
*   **[Plotly](https://plotly.com/python/)**: Used for creating interactive and responsive maps and charts.
*   **[Pandas](https://pandas.pydata.org/)**: For robust data manipulation and cleaning.
*   **[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)**: For a responsive, mobile-friendly layout and themed components.
*   **[Flask-Caching](https://flask-caching.readthedocs.io/)**: To optimize performance through intelligent data caching.

## Getting Started

1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python app.py
    ```
4.  Open your browser and navigate to `http://127.0.0.1:8050`.
