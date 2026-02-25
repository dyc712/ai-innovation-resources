#!/usr/bin/env python3
"""
美股投资标的2.0自动更新脚本 V4
功能：获取真实股票数据并更新2.0分析指标
数据源：富途OpenAPI（主） + yfinance（备用） + Polygon.io（历史回测）
新增功能：QQQ/SPY指数跟踪，辅助个股波段操作
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import time
import json
import requests
import warnings
from typing import Dict, Optional, List
warnings.filterwarnings('ignore')

# ==================== 配置区 ====================

# Polygon.io API配置（用于历史数据回测）
POLYGON_API_KEY = "YOUR_POLYGON_API_KEY"  # 需要用户提供
POLYGON_BASE_URL = "https://api.polygon.io"

# 异动阈值配置
ABNORMAL_THRESHOLD = 5.0  # 单日涨跌幅超过5%视为异动

# 富途OpenD配置
FUTU_HOST = "127.0.0.1"
FUTU_PORT = 11111  # FutuOpenD默认端口

# 指数ETF代码
INDEX_TICKERS = {
    'QQQ': '纳斯达克100指数ETF',
    'SPY': '标普500指数ETF'
}

# ==================== 富途OpenAPI数据获取 ====================

def init_futu_connection():
    """初始化富途OpenAPI连接"""
    try:
        from futu import OpenQuoteContext, RET_OK
        
        quote_ctx = OpenQuoteContext(host=FUTU_HOST, port=FUTU_PORT)
        print(f"✅ 富途OpenD连接成功: {FUTU_HOST}:{FUTU_PORT}")
        return quote_ctx
    except ImportError:
        print("⚠️  futu-api未安装，将使用备用数据源")
        return None
    except Exception as e:
        print(f"⚠️  富途OpenD连接失败: {str(e)}")
        print("💡 请确保FutuOpenD网关已启动并监听 127.0.0.1:11111")
        return None

def fetch_from_futu(quote_ctx, ticker: str) -> Optional[Dict]:
    """从富途OpenAPI获取股票数据"""
    if quote_ctx is None:
        return None
    
    try:
        from futu import RET_OK, Market
        
        # 转换ticker为富途格式（US.XXX）
        futu_ticker = f"US.{ticker}"
        
        # 获取实时报价
        ret, data = quote_ctx.get_market_snapshot([futu_ticker])
        
        if ret != RET_OK:
            print(f"  富途API错误: {data}")
            return None
        
        if data.empty:
            return None
        
        row = data.iloc[0]
        current_price = row['last_price']
        prev_close = row['prev_close_price']
        
        price_change_1d = ((current_price / prev_close) - 1) * 100 if prev_close > 0 else 0
        
        # 获取历史K线数据（用于技术指标计算）
        from futu import KLType
        ret_kline, kline_data = quote_ctx.get_cur_kline(futu_ticker, 100, KLType.K_DAY)
        
        hist_data = None
        if ret_kline == RET_OK and not kline_data.empty:
            hist_data = kline_data[['close', 'high', 'low', 'volume']].copy()
            hist_data.columns = ['Close', 'High', 'Low', 'Volume']
        
        return {
            'source': 'futu',
            'current_price': round(current_price, 2),
            'high': row.get('high_price', current_price),
            'low': row.get('low_price', current_price),
            'open': row.get('open_price', current_price),
            'prev_close': prev_close,
            'price_change_1d': round(price_change_1d, 2),
            'volume': row.get('volume', 0),
            'hist_data': hist_data  # 用于技术指标计算
        }
    except Exception as e:
        print(f"  富途API错误: {str(e)}")
        return None

# ==================== Yahoo Finance优化版 ====================

def fetch_from_yfinance_optimized(ticker: str) -> Optional[Dict]:
    """
    优化版yfinance获取（模拟浏览器行为，延长超时）
    """
    try:
        import requests_cache
        
        # 创建Session，模拟浏览器
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        })
        
        # 使用Session模式，延长超时到60秒
        stock = yf.Ticker(ticker, session=session)
        hist = stock.history(period="5d", timeout=60)
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        price_change_1d = ((current_price / prev_close) - 1) * 100 if prev_close > 0 else 0
        
        # 获取更长历史数据用于技术指标
        hist_3m = stock.history(period="3mo", timeout=60)
        
        return {
            'source': 'yfinance',
            'current_price': round(current_price, 2),
            'high': hist['High'].iloc[-1],
            'low': hist['Low'].iloc[-1],
            'open': hist['Open'].iloc[-1],
            'prev_close': prev_close,
            'price_change_1d': round(price_change_1d, 2),
            'volume': hist['Volume'].iloc[-1],
            'hist_data': hist_3m  # 3个月历史数据
        }
    except Exception as e:
        print(f"  yfinance错误: {str(e)}")
        return None

# ==================== Polygon.io历史数据获取 ====================

def fetch_from_polygon(ticker: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    从Polygon.io获取历史数据（用于回测）
    """
    if POLYGON_API_KEY == "YOUR_POLYGON_API_KEY":
        return None
    
    try:
        url = f"{POLYGON_BASE_URL}/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
        params = {
            'adjusted': 'true',
            'sort': 'asc',
            'apiKey': POLYGON_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'OK' and 'results' in data:
                df = pd.DataFrame(data['results'])
                df['date'] = pd.to_datetime(df['t'], unit='ms')
                df = df.rename(columns={
                    'o': 'open',
                    'h': 'high',
                    'l': 'low',
                    'c': 'close',
                    'v': 'volume'
                })
                return df[['date', 'open', 'high', 'low', 'close', 'volume']]
        
        return None
    except Exception as e:
        print(f"  Polygon.io错误: {str(e)}")
        return None

# ==================== 指数数据获取 ====================

def fetch_index_data(ticker: str) -> Optional[Dict]:
    """获取指数ETF数据（QQQ/SPY）"""
    print(f"\n📊 获取指数数据: {ticker} - {INDEX_TICKERS[ticker]}")
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="3mo", timeout=60)
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        
        # 计算技术指标
        sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
        sma_60 = hist['Close'].rolling(60).mean().iloc[-1] if len(hist) >= 60 else sma_20
        
        # 趋势判断
        if current_price > sma_20 > sma_60:
            trend = "多头排列"
            trend_signal = 1  # 支持做多
        elif current_price > sma_20:
            trend = "震荡偏多"
            trend_signal = 0.5
        elif current_price < sma_20 < sma_60:
            trend = "空头排列"
            trend_signal = -1  # 避免做多
        else:
            trend = "震荡"
            trend_signal = 0
        
        # 计算动量
        price_change_20d = ((current_price / hist['Close'].iloc[-21]) - 1) * 100 if len(hist) > 20 else 0
        
        return {
            'ticker': ticker,
            'name': INDEX_TICKERS[ticker],
            'current_price': round(current_price, 2),
            'sma_20': round(sma_20, 2),
            'sma_60': round(sma_60, 2),
            'trend': trend,
            'trend_signal': trend_signal,
            'price_change_20d': round(price_change_20d, 2)
        }
    except Exception as e:
        print(f"❌ {ticker}获取失败: {str(e)}")
        return None

# ==================== 综合数据获取（主函数）====================

def fetch_stock_data(quote_ctx, ticker: str, retries: int = 3) -> Optional[Dict]:
    """
    综合数据获取策略：富途 → yfinance优化版
    """
    for attempt in range(retries):
        try:
            # 1. 优先使用富途OpenAPI
            if quote_ctx is not None:
                print(f"  尝试富途...", end='')
                basic_data = fetch_from_futu(quote_ctx, ticker)
                
                if basic_data is not None:
                    print(f" ✅ [富途]")
                    return process_market_data(basic_data, ticker)
            
            # 2. 备用：优化版yfinance
            print(f"  切换yfinance(优化版)...", end='')
            basic_data = fetch_from_yfinance_optimized(ticker)
            
            if basic_data is not None:
                print(f" ✅ [yfinance]")
                return process_market_data(basic_data, ticker)
            
            # 重试逻辑
            if attempt < retries - 1:
                print(f" 重试{attempt+1}/{retries}...")
                time.sleep(3)  # 增加延迟
                continue
            else:
                print(f" ❌ 所有数据源均失败")
                return None
                
        except Exception as e:
            if attempt < retries - 1:
                print(f"⚠️  {ticker}: 重试 {attempt + 1}/{retries}... ({str(e)})")
                time.sleep(3)
            else:
                print(f"❌ {ticker}: 获取失败 - {str(e)}")
                return None

def process_market_data(basic_data: Dict, ticker: str) -> Dict:
    """处理市场数据，计算技术指标"""
    
    hist = basic_data.get('hist_data')
    
    if hist is None or hist.empty:
        # 如果没有历史数据，尝试用yfinance补充
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo", timeout=60)
        except:
            hist = pd.DataFrame()
    
    current_price = basic_data['current_price']
    
    # 计算ATR (14日)
    try:
        high_low = hist['High'] - hist['Low']
        high_close = abs(hist['High'] - hist['Close'].shift())
        low_close = abs(hist['Low'] - hist['Close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(14).mean().iloc[-1]
    except:
        atr = current_price * 0.02  # 默认2%作为ATR
    
    # 计算RS相对强度（vs SPY）
    try:
        spy = yf.Ticker("SPY").history(period="3mo", timeout=60)
        stock_return = (current_price / hist['Close'].iloc[0] - 1) * 100
        spy_return = (spy['Close'].iloc[-1] / spy['Close'].iloc[0] - 1) * 100
        rs_score = stock_return - spy_return
    except:
        rs_score = 0
    
    # 计算动量指标
    try:
        sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
        sma_60 = hist['Close'].rolling(60).mean().iloc[-1] if len(hist) >= 60 else sma_20
        
        momentum_score = 0
        if current_price > sma_20 > sma_60:
            momentum_score = 10  # 均线多头排列
        elif current_price > sma_20:
            momentum_score = 5
        elif current_price < sma_20 < sma_60:
            momentum_score = -10  # 均线空头排列
    except:
        sma_20 = current_price
        sma_60 = current_price
        momentum_score = 0
    
    # 计算成交量趋势
    try:
        vol_ma_20 = hist['Volume'].rolling(20).mean().iloc[-1]
        current_vol = hist['Volume'].iloc[-1]
        volume_signal = 5 if current_vol > vol_ma_20 * 1.5 else 0
    except:
        volume_signal = 0
    
    # 获取机构持仓数据（yfinance）
    try:
        stock = yf.Ticker(ticker)
        institutional_holders = stock.institutional_holders
        institution_score = 10 if institutional_holders is not None and len(institutional_holders) > 0 else 0
    except:
        institution_score = 0
    
    # 获取分析师评级
    try:
        stock = yf.Ticker(ticker)
        recommendations = stock.recommendations
        if recommendations is not None and len(recommendations) > 0:
            recent = recommendations.tail(5)
            buy_count = len(recent[recent['To Grade'].str.contains('Buy|Outperform', case=False, na=False)])
            analyst_score = min(10, buy_count * 2)
        else:
            analyst_score = 0
    except:
        analyst_score = 0
    
    # 计算价格变动
    price_change_1d = basic_data['price_change_1d']
    try:
        price_change_5d = ((current_price / hist['Close'].iloc[-6]) - 1) * 100 if len(hist) > 5 else 0
    except:
        price_change_5d = 0
    
    return {
        'current_price': round(current_price, 2),
        'atr': round(atr, 2),
        'rs_score': round(rs_score, 2),
        'momentum_score': momentum_score,
        'volume_signal': volume_signal,
        'institution_score': institution_score,
        'analyst_score': analyst_score,
        'price_change_1d': round(price_change_1d, 2),
        'price_change_5d': round(price_change_5d, 2),
        'sma_20': round(sma_20, 2),
        'sma_60': round(sma_60, 2),
        'data_source': basic_data['source']
    }

# ==================== 异动原因分析 ====================

def fetch_abnormal_reason(ticker: str, price_change: float) -> str:
    """收集异动原因分析"""
    reasons = []
    
    try:
        stock = yf.Ticker(ticker)
        
        # 1. 获取最新新闻
        try:
            news = stock.news
            if news and len(news) > 0:
                news_headlines = []
                for item in news[:3]:
                    headline = item.get('title', '')
                    if headline:
                        news_headlines.append(f"📰 {headline}")
                
                if news_headlines:
                    reasons.append("**最新新闻**:\n" + "\n".join(news_headlines))
        except:
            pass
        
        # 2. 检查财报发布
        try:
            earnings = stock.earnings_dates
            if earnings is not None and len(earnings) > 0:
                recent_earnings = earnings.head(1)
                earnings_date = recent_earnings.index[0]
                if (datetime.now() - earnings_date).days <= 5:
                    reasons.append(f"📊 **财报发布**: {earnings_date.strftime('%Y-%m-%d')}")
        except:
            pass
        
        # 3. 检查分析师评级变化
        try:
            recommendations = stock.recommendations
            if recommendations is not None and len(recommendations) > 0:
                recent = recommendations.tail(3)
                recent_date = recent.index[-1]
                if (datetime.now() - recent_date).days <= 5:
                    to_grade = recent.iloc[-1]['To Grade']
                    firm = recent.iloc[-1]['Firm']
                    reasons.append(f"⭐ **分析师评级**: {firm} 给予 {to_grade}")
        except:
            pass
        
        # 4. 市场情绪判断
        if price_change > 10:
            reasons.append("🚀 **市场情绪**: 强势拉升，可能受利好催化")
        elif price_change > 5:
            reasons.append("📈 **市场情绪**: 积极上涨，关注持续性")
        elif price_change < -10:
            reasons.append("💔 **市场情绪**: 恐慌性下跌，警惕连锁反应")
        elif price_change < -5:
            reasons.append("📉 **市场情绪**: 显著下跌，注意风险")
        
        # 5. 技术面判断（成交量）
        hist = stock.history(period="5d")
        if len(hist) >= 2:
            volume_increase = (hist['Volume'].iloc[-1] / hist['Volume'].iloc[-2] - 1) * 100
            if volume_increase > 100:
                reasons.append(f"📊 **成交量异动**: 放量{volume_increase:.0f}%（可能有资金博弈）")
        
    except Exception as e:
        reasons.append(f"⚠️ 原因分析获取失败: {str(e)}")
    
    if not reasons:
        if abs(price_change) > 5:
            reasons.append("❓ **暂无明确消息**，建议关注盘后新闻和市场解读")
    
    return "\n".join(reasons) if reasons else "无异动原因"

# ==================== 评分计算（加入指数判断）====================

def calculate_scores(row, market_data: Dict, index_signals: Dict) -> Optional[Dict]:
    """计算2.0评分体系（增加指数辅助判断）"""
    
    if market_data is None:
        return None
    
    # === 宏观风控（新增指数判断）===
    macro_penalty = 0
    
    # 指数市场环境评分
    index_score = 0
    if index_signals:
        qqq_signal = index_signals.get('QQQ', {}).get('trend_signal', 0)
        spy_signal = index_signals.get('SPY', {}).get('trend_signal', 0)
        
        # 平均指数信号
        avg_index_signal = (qqq_signal + spy_signal) / 2
        
        if avg_index_signal >= 0.75:
            index_score = 10  # 指数强势，适合做多
        elif avg_index_signal >= 0:
            index_score = 5  # 指数偏多
        elif avg_index_signal >= -0.5:
            index_score = 0  # 中性
        else:
            index_score = -10  # 指数弱势，避免做多
            macro_penalty = 10
    
    # === 技术面 (40分) ===
    rs_score_tech = 0
    if market_data['rs_score'] > 10:
        rs_score_tech = 10
    elif market_data['rs_score'] > 0:
        rs_score_tech = 5
    elif market_data['rs_score'] < -10:
        rs_score_tech = -10
    
    vap_score = market_data['volume_signal']
    momentum = market_data['momentum_score']
    
    tech_total = 20 + rs_score_tech + vap_score + momentum
    tech_total = max(0, min(40, tech_total))
    
    # === 资金面 (40分) ===
    institution = market_data['institution_score']
    chips_score = 5 if market_data['price_change_5d'] > 0 else -5
    short_score = 5
    
    funds_total = 20 + institution + chips_score + short_score
    funds_total = max(0, min(40, funds_total))
    
    # === 消息面 (20分) ===
    catalyst_score = 0
    analyst = market_data['analyst_score']
    sentiment = 0
    
    info_total = 10 + catalyst_score + analyst + sentiment
    info_total = max(0, min(20, info_total))
    
    # === 综合评分（含指数加权）===
    base_score = int((0.4 * tech_total) + (0.4 * funds_total) + (0.2 * info_total))
    total_score = max(0, min(100, base_score + index_score - macro_penalty))
    
    # === 风控计算 ===
    current_price = market_data['current_price']
    atr = market_data['atr']
    
    category = row['分类'] if pd.notna(row['分类']) else ''
    if '核能' in category or '稀土' in category or 'ASIC' in category:
        n_value = 2.5
    else:
        n_value = 1.5
    
    stop_loss = round(current_price - (n_value * atr), 2)
    tp1 = round(current_price + (1.0 * atr), 2)
    tp2 = round(current_price + (2.5 * atr), 2)
    
    risk = current_price - stop_loss
    reward = tp2 - current_price
    rrr = round(reward / risk, 2) if risk > 0 else 0
    
    # === 价格区间判断（加入指数判断）===
    sma_60 = market_data.get('sma_60', market_data['current_price'])
    
    # 指数环境好 + 个股技术面好 = 买入狙击区
    if avg_index_signal >= 0.5 and rs_score_tech >= 10 and momentum > 5:
        price_zone = '买入狙击区'
    elif avg_index_signal >= 0.5 and rs_score_tech >= 5 and momentum >= 0:
        price_zone = '加仓确认区'
    elif avg_index_signal < 0 or (rs_score_tech < 0 and momentum < 0):
        price_zone = '深度回调区'
    elif market_data['current_price'] > sma_60:
        price_zone = '持仓观察区'
    else:
        price_zone = '待评估'
    
    # === 操盘建议（加入指数限制）===
    # 如果指数空头排列，降低评级
    if avg_index_signal < -0.5:
        action = '【观望/减仓】'
        position = '0-20%'
        priority = 'C级'
    elif total_score >= 80 and price_zone == '买入狙击区' and rrr >= 2.5:
        action = '【强力买入】'
        position = '60-80%'
        priority = 'A级'
    elif total_score >= 80 and price_zone == '加仓确认区' and rrr >= 2.5:
        action = '【追涨/加仓】'
        position = '20%'
        priority = 'A级'
    elif 60 <= total_score < 80 and price_zone == '买入狙击区' and rrr >= 2.5:
        action = '【试探买入】'
        position = '30-50%'
        priority = 'B级'
    elif 60 <= total_score < 80 and rrr >= 2.5:
        action = '【持有】'
        position = '维持'
        priority = 'B级'
    elif total_score < 60 or rrr < 2.5:
        action = '【观望/卖出】'
        position = '0%'
        priority = 'C级'
    else:
        action = '【观望】'
        position = '0-10%'
        priority = 'C级'
    
    # 构建状态描述
    rs_status = 'RS超越大盘' if market_data['rs_score'] > 10 else ('RS跟随大盘' if market_data['rs_score'] > 0 else 'RS弱于大盘')
    momentum_status = '均线多头' if momentum > 5 else ('震荡' if momentum >= -5 else '均线空头')
    
    return {
        'current_price': current_price,
        'atr': atr,
        'tech_total': f'{tech_total}/40',
        'funds_total': f'{funds_total}/40',
        'info_total': f'{info_total}/20',
        'total_score': total_score,
        'index_score': index_score,  # 新增
        'rs_status': rs_status,
        'momentum_status': momentum_status,
        'price_zone': price_zone,
        'action': action,
        'position': position,
        'priority': priority,
        'stop_loss': f'${stop_loss}',
        'tp1': f'${tp1}',
        'tp2': f'${tp2}',
        'rrr': rrr,
        'price_change_1d': f'{market_data["price_change_1d"]:+.2f}%',
        'price_change_5d': f'{market_data["price_change_5d"]:+.2f}%'
    }

# ==================== 主程序 ====================

def main():
    print("=" * 80)
    print("🚀 美股投资标的2.0自动更新任务启动 [V4]")
    print("=" * 80)
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📡 数据源: 富途OpenAPI（主） + yfinance优化版（备用） + Polygon.io（回测）")
    print()
    
    # 初始化富途连接
    quote_ctx = init_futu_connection()
    
    # === 第一步：获取指数数据 ===
    print("\n" + "=" * 80)
    print("📊 第一步：获取指数市场环境")
    print("=" * 80)
    
    index_signals = {}
    for ticker in INDEX_TICKERS.keys():
        index_data = fetch_index_data(ticker)
        if index_data:
            index_signals[ticker] = index_data
            print(f"✅ {ticker}: {index_data['current_price']} | {index_data['trend']} | 20日涨跌: {index_data['price_change_20d']:+.2f}%")
        else:
            print(f"❌ {ticker}: 获取失败")
    
    # 打印市场环境判断
    if index_signals:
        print("\n🌐 **市场环境判断**:")
        qqq_signal = index_signals.get('QQQ', {}).get('trend_signal', 0)
        spy_signal = index_signals.get('SPY', {}).get('trend_signal', 0)
        avg_signal = (qqq_signal + spy_signal) / 2
        
        if avg_signal >= 0.75:
            env_status = "🟢 强势多头，适合积极做多"
        elif avg_signal >= 0:
            env_status = "🟡 偏多环境，谨慎做多"
        elif avg_signal >= -0.5:
            env_status = "🟠 震荡市，控制仓位"
        else:
            env_status = "🔴 弱势空头，避免做多"
        
        print(f"  {env_status}")
        print(f"  QQQ信号: {qqq_signal:+.2f} | SPY信号: {spy_signal:+.2f}")
    
    # === 第二步：读取个股清单 ===
    print("\n" + "=" * 80)
    print("📊 第二步：更新个股数据")
    print("=" * 80)
    
    excel_file = '/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ 文件不存在: {excel_file}")
        if quote_ctx:
            quote_ctx.close()
        return
    
    df = pd.read_excel(excel_file)
    print(f"📊 读取到 {len(df)} 只股票")
    print()
    
    # 获取所有股票的实时数据
    success_count = 0
    failed_tickers = []
    data_source_stats = {'futu': 0, 'yfinance': 0}
    
    results = []
    abnormal_stocks = []
    
    for idx, row in df.iterrows():
        ticker = row['股票代码']
        print(f"[{idx+1}/{len(df)}] 正在获取 {ticker} 数据...", end=' ')
        
        market_data = fetch_stock_data(quote_ctx, ticker)
        
        if market_data:
            scores = calculate_scores(row, market_data, index_signals)
            if scores:
                results.append({
                    'ticker': ticker,
                    'data': market_data,
                    'scores': scores
                })
                success_count += 1
                data_source_stats[market_data['data_source']] += 1
                
                # 打印结果（增加指数评分）
                index_bonus = f" | 指数加分{scores['index_score']:+d}" if scores['index_score'] != 0 else ""
                print(f"✅ ${scores['current_price']:.2f} | 评分: {scores['total_score']}{index_bonus} | {scores['priority']}")
                
                # 检测异动
                price_change = market_data['price_change_1d']
                if abs(price_change) >= ABNORMAL_THRESHOLD:
                    print(f"   🔔 检测到异动 ({price_change:+.2f}%)，正在分析原因...")
                    reason = fetch_abnormal_reason(ticker, price_change)
                    abnormal_stocks.append({
                        'ticker': ticker,
                        'name': row.get('股票名称', ticker),
                        'category': row.get('分类', ''),
                        'price': scores['current_price'],
                        'change': price_change,
                        'reason': reason,
                        'score': scores['total_score'],
                        'priority': scores['priority']
                    })
                    time.sleep(1)
            else:
                failed_tickers.append(ticker)
                print("❌ 评分计算失败")
        else:
            failed_tickers.append(ticker)
        
        # 避免API限流
        time.sleep(2)
    
    print()
    print("=" * 80)
    print(f"✅ 数据获取完成: {success_count}/{len(df)} 成功 ({success_count/len(df)*100:.1f}%)")
    print(f"📡 数据源统计: 富途 {data_source_stats['futu']}只 | yfinance {data_source_stats['yfinance']}只")
    if failed_tickers:
        print(f"❌ 失败标的: {', '.join(failed_tickers)}")
    print("=" * 80)
    print()
    
    # === 第三步：更新Excel ===
    for result in results:
        ticker = result['ticker']
        idx = df[df['股票代码'] == ticker].index[0]
        
        # 更新基础数据
        df.at[idx, '当天价格'] = result['scores']['current_price']
        df.at[idx, 'ATR波动率'] = result['scores']['atr']
        
        # 更新评分
        df.at[idx, '技术面得分'] = result['scores']['tech_total']
        df.at[idx, '资金面得分'] = result['scores']['funds_total']
        df.at[idx, '消息面得分'] = result['scores']['info_total']
        df.at[idx, '总评分'] = result['scores']['total_score']
        
        # 更新状态
        df.at[idx, 'RS相对强度'] = result['scores']['rs_status']
        df.at[idx, '趋势动量共振'] = result['scores']['momentum_status']
        df.at[idx, '价格区间判断'] = result['scores']['price_zone']
        
        # 更新操盘建议
        df.at[idx, '操盘建议'] = result['scores']['action']
        df.at[idx, '建议仓位'] = result['scores']['position']
        df.at[idx, '执行优先级'] = result['scores']['priority']
        
        # 更新风控
        df.at[idx, '动态止损位'] = result['scores']['stop_loss']
        df.at[idx, '第一止盈位'] = result['scores']['tp1']
        df.at[idx, '目标止盈位'] = result['scores']['tp2']
        df.at[idx, '风险收益比2.0'] = result['scores']['rrr']
        
        # 更新价格变动
        df.at[idx, '日涨跌幅'] = result['scores']['price_change_1d']
        df.at[idx, '周涨跌幅'] = result['scores']['price_change_5d']
    
    # 添加更新时间
    df['最后更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 保存Excel
    output_file = '/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"💾 数据已保存: {output_file}")
    print()
    
    # === 第四步：生成报告 ===
    a_grade = df[df['执行优先级'] == 'A级'].sort_values('总评分', ascending=False) if '执行优先级' in df.columns else pd.DataFrame()
    b_grade = df[df['执行优先级'] == 'B级'].sort_values('总评分', ascending=False) if '执行优先级' in df.columns else pd.DataFrame()
    
    # 找出价格异动标的
    price_movers = []
    for result in results:
        change_val = float(result['scores']['price_change_1d'].replace('%', '').replace('+', ''))
        if abs(change_val) > 5:
            price_movers.append({
                'ticker': result['ticker'],
                'change': result['scores']['price_change_1d']
            })
    
    # 生成报告
    report = f"""
📊 **美股投资标的2.0更新报告 [V4]**
⏰ 更新时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
📡 数据源: 富途OpenAPI + yfinance优化版

### 🌐 市场环境分析
"""
    
    if index_signals:
        report += "\n#### 指数技术面\n"
        for ticker, data in index_signals.items():
            signal_emoji = "🟢" if data['trend_signal'] >= 0.75 else ("🟡" if data['trend_signal'] >= 0 else "🔴")
            report += f"- **{ticker}** ({data['name']}): ${data['current_price']} | {signal_emoji} {data['trend']} | 20日涨跌: {data['price_change_20d']:+.2f}%\n"
        
        report += f"\n**环境结论**: {env_status}\n"
    
    report += f"""
### 📈 更新概况
- 成功更新: {success_count}/{len(df)} 只 ({success_count/len(df)*100:.1f}%)
- 失败标的: {len(failed_tickers)} 只
- 数据源: 富途 {data_source_stats['futu']}只 | yfinance {data_source_stats['yfinance']}只

### 🎯 执行优先级分布
- A级（强力买入/追涨）: {len(a_grade)} 只
- B级（试探买入/持有）: {len(b_grade)} 只
- C级（观望/卖出）: {len(df) - len(a_grade) - len(b_grade)} 只

"""
    
    if len(a_grade) > 0:
        report += "\n### 🔥 A级推荐标的\n"
        for _, row in a_grade.iterrows():
            report += f"- **{row['股票代码']}** ({row['分类']}): ${row['当天价格']:.2f} | 评分{row['总评分']}分 | {row['操盘建议']} | RRR={row['风险收益比2.0']}\n"
    
    if len(b_grade) > 0:
        report += "\n### 📌 B级关注标的\n"
        for _, row in b_grade.head(5).iterrows():
            report += f"- **{row['股票代码']}**: ${row['当天价格']:.2f} | 评分{row['总评分']}分 | {row['价格区间判断']}\n"
    
    if price_movers:
        report += "\n### ⚡ 价格异动提醒（单日涨跌>5%）\n"
        for mover in price_movers[:5]:
            report += f"- **{mover['ticker']}**: {mover['change']}\n"
    
    # 异动原因分析
    if abnormal_stocks:
        report += "\n### 🔍 异动原因深度分析\n"
        report += f"*共检测到 {len(abnormal_stocks)} 只异动标的*\n\n"
        
        abnormal_stocks.sort(key=lambda x: abs(x['change']), reverse=True)
        
        for idx, stock in enumerate(abnormal_stocks[:8], 1):
            emoji = "📈" if stock['change'] > 0 else "📉"
            report += f"#### {idx}. {emoji} **{stock['ticker']}** - {stock['name']} ({stock['category']})\n"
            report += f"- **价格**: ${stock['price']} | **涨跌**: {stock['change']:+.2f}% | **评分**: {stock['score']}分 | **优先级**: {stock['priority']}\n"
            report += f"- **异动原因**:\n{stock['reason']}\n\n"
    
    if failed_tickers:
        report += f"\n### ⚠️ 更新失败标的\n{', '.join(failed_tickers)}\n"
    
    report += "\n---\n*数据源: 富途OpenAPI (主) + yfinance优化版 (备用) + Polygon.io (回测) | 分析框架: 专业作手2.0体系 + 指数辅助判断*"
    
    print(report)
    
    # 保存报告
    report_file = f'/data/workspace/美股2.0更新报告_{datetime.now().strftime("%Y%m%d_%H%M")}.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 报告已保存: {report_file}")
    print("=" * 80)
    
    # 关闭富途连接
    if quote_ctx:
        quote_ctx.close()
        print("✅ 富途连接已关闭")
    
    return report

if __name__ == '__main__':
    try:
        report = main()
        
        # 输出报告供notify工具使用
        print("\n[REPORT_FOR_NOTIFY]")
        print(report)
        
    except Exception as e:
        error_msg = f"❌ 更新任务执行失败: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        print("[REPORT_FOR_NOTIFY]")
        print(error_msg)
        sys.exit(1)
