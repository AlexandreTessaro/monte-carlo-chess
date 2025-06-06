import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Usar o arquivo gerado pela simulação anterior
df = pd.DataFrame({
    "opening": ["e4", "d4", "Sicilian Defense", "Ruy Lopez"],
    "white_win_rate": [0.4757, 0.4795, 0.4698, 0.4978],
    "black_win_rate": [0.4794, 0.4807, 0.4903, 0.4653],
    "draw_rate":      [0.0449, 0.0398, 0.0399, 0.0369]
})

# Configuração estética
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Gráfico de barras agrupadas
df_melted = df.melt(id_vars="opening", value_vars=["white_win_rate", "black_win_rate", "draw_rate"],
                    var_name="Result", value_name="Rate")

sns.barplot(data=df_melted, x="opening", y="Rate", hue="Result", palette="Set2")

plt.title("Monte Carlo Simulation: Win/Draw Rates by Opening")
plt.ylabel("Rate")
plt.xlabel("Opening")
plt.ylim(0, 0.55)
plt.legend(title="Outcome")
plt.tight_layout()
plt.show()
