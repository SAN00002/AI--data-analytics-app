import pandas as pd
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


class DataAgent:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def get_overview(self):
        rows, cols = self.df.shape
        return f"Dataset has {rows} rows and {cols} columns"

    def get_missing(self):
        return self.df.isnull().sum()

    def get_summary(self):
        return self.df.describe()

    def generate_insights(self):
        insights = []

        missing = self.df.isnull().sum()
        if missing.sum() > 0:
            insights.append("Dataset contains missing values.")

        numeric_cols = self.df.select_dtypes(include="number").columns
        for col in numeric_cols:
            if self.df[col].mean() > self.df[col].median():
                insights.append(f"{col} is slightly right-skewed.")

        if len(numeric_cols) > 0:
            high_var = self.df[numeric_cols].var().idxmax()
            insights.append(f"{high_var} shows highest variability.")

        return insights

    def plot_all_numeric(self):
        numeric_cols = self.df.select_dtypes(include="number").columns

        for col in numeric_cols:
            self.df[col].plot()
            plt.title(col)
            plt.savefig(f"{col}.png")
            plt.clf()

        return numeric_cols

    def correlation_heatmap(self):
        corr = self.df.corr(numeric_only=True)

        plt.imshow(corr)
        plt.colorbar()
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig("heatmap.png")
        plt.clf()

        return "Heatmap created"
    
    def detect_outliers(self):
        numeric_cols = self.df.select_dtypes(include="number").columns
        outlier_summary = {}

        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)]
            outlier_summary[col] = len(outliers)

        return outlier_summary


    def plot_outliers(self):
        numeric_cols = self.df.select_dtypes(include="number").columns

        for col in numeric_cols:
            self.df.boxplot(column=col)
            plt.title(f"Outliers in {col}")
            plt.savefig(f"{col}_outliers.png")
            plt.clf()

        return numeric_cols
    
    def chat(self, question):
        q = question.lower()

        if "average" in q or "mean" in q:
            return self.df.mean(numeric_only=True).to_string()

        if "max" in q:
            return self.df.max(numeric_only=True).to_string()

        if "min" in q:
            return self.df.min(numeric_only=True).to_string()

        if "columns" in q:
            return str(self.df.columns.tolist())

        return "Try asking about averages, max, min, or columns."


    def generate_pdf_report(self):
        doc = SimpleDocTemplate("report.pdf")
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Data Analysis Report", styles["Title"]))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(self.get_overview(), styles["Normal"]))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Summary Statistics", styles["Heading2"]))
        elements.append(Paragraph(self.df.describe().to_string(), styles["Normal"]))

        doc.build(elements)
        return "report.pdf"
   