from func_calculation_static import calculate_cointegration_static, calculate_spread_static, calculate_z_score_window
from binance_market_observer import binance_get_recent_close_price
import pandas as pd
from config import TRIGGER_Z_SCORE_THRESHOD, Z_SCORE_WINDOW, INTERVAL, TRADING_TIME_LIMIT_INTERVALS
import matplotlib.pyplot as plt
import json

def plot_reference(sym_1, sym_2, num_wave=0):
    with open("15m_price_list.json", "r")as price_data:
        data = json.load(price_data)
        price_symbol_1 = data[sym_1]
        price_symbol_2 = data[sym_2]
    
    coint_flag, p_value, hedge_ratio, initial_intercept = calculate_cointegration_static(price_symbol_1, price_symbol_2)
    spread = calculate_spread_static(price_symbol_1, price_symbol_2, hedge_ratio)
    z_score = calculate_z_score_window(spread, Z_SCORE_WINDOW)
    
        # Calculate percentage changes
    df = pd.DataFrame(columns=[sym_1, sym_2])
    df[sym_1] = price_symbol_1
    df[sym_2] = price_symbol_2
    df[f"{sym_1}_pct"] = df[sym_1] / price_symbol_1[0]
    df[f"{sym_2}_pct"] = df[sym_2] / price_symbol_2[0]
    series_1 = df[f"{sym_1}_pct"].astype(float).values
    series_2 = df[f"{sym_2}_pct"].astype(float).values
    
    fig, axs = plt.subplots(3, figsize = (16, 8))
    fig.suptitle(f"Price, Spread and Z_score - {sym_1} vs {sym_2}")
    axs[0].plot(series_1, label = f"{sym_1}")
    axs[0].plot(series_2, label = f"{sym_2}")
    axs[0].title.set_text("Price percentage change")
    axs[0].legend()
    axs[1].plot(spread)
    axs[1].title.set_text("Spread")
    axs[2].plot(z_score)
    axs[2].axhline(y=TRIGGER_Z_SCORE_THRESHOD, color='r', linestyle='dotted')
    axs[2].axhline(y=-TRIGGER_Z_SCORE_THRESHOD, color='r', linestyle='dotted')
    axs[2].axhline(y=0, color='g', linestyle='-')
    axs[2].title.set_text("Z score")
    plt.savefig(f"{num_wave}_wave_trading_pair_history_graph.png")

# plot_reference("ZILUSDT", "1000XECUSDT")
# with open("15m_price_list.json", "r")as price_data:
#     print(price_data["BTCUSDT"])


def plot_reference_trading(symbol_1, symbol_2, hedge_ratio, num_wave=0):

    price_symbol_1 = binance_get_recent_close_price(symbol_1, INTERVAL, Z_SCORE_WINDOW + TRADING_TIME_LIMIT_INTERVALS)
    price_symbol_2 = binance_get_recent_close_price(symbol_2, INTERVAL, Z_SCORE_WINDOW + TRADING_TIME_LIMIT_INTERVALS)
    
    spread = calculate_spread_static(price_symbol_1, price_symbol_2, hedge_ratio)
    z_score = calculate_z_score_window(spread, Z_SCORE_WINDOW)
    
        # Calculate percentage changes
    df = pd.DataFrame(columns=[symbol_1, symbol_2])
    df[symbol_1] = price_symbol_1
    df[symbol_2] = price_symbol_2
    df[f"{symbol_1}_pct"] = df[symbol_1] / price_symbol_1[0]
    df[f"{symbol_2}_pct"] = df[symbol_2] / price_symbol_2[0]
    series_1 = df[f"{symbol_1}_pct"].astype(float).values
    series_2 = df[f"{symbol_2}_pct"].astype(float).values
    
    fig, axs = plt.subplots(3, figsize = (16, 8))
    fig.suptitle(f"Price, Spread and Z_score - {symbol_1} vs {symbol_2}")
    axs[0].plot(series_1, label = f"{symbol_1}")
    axs[0].plot(series_2, label = f"{symbol_2}")
    axs[0].title.set_text("Price percentage change")
    axs[0].legend()
    axs[1].plot(spread)
    axs[1].title.set_text("Spread")
    axs[2].plot(z_score)
    axs[2].axhline(y=TRIGGER_Z_SCORE_THRESHOD, color='r', linestyle='dotted')
    axs[2].axhline(y=-TRIGGER_Z_SCORE_THRESHOD, color='r', linestyle='dotted')
    axs[2].axhline(y=0, color='g', linestyle='-')
    axs[2].title.set_text("Z score")
    plt.savefig(f"{num_wave}_wave_trading_pair_trading_graph.png")

# plot_reference_trading("ZILUSDT", "1000XECUSDT", 1, num_wave=0)