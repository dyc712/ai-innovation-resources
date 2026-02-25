#!/usr/bin/env python3
"""
美股投资标的2.0自动更新脚本 V2
功能：获取真实股票数据并更新2.0分析指标
数据源：Finnhub API（主） + yfinance（备用）
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
warnings.filterwarnings('ignore')

# Finnhub API配置（免费API密钥）
FINNHUB_API_KEY = "ctp96o9r01qnbe8ij99gctp96o9r01qnbe8ij9a0"  # 免费API密钥
FINNHUB_BASE_URL = "https://finnhub.io/api/v1"

# 异动阈值配置
ABNORMAL_THRESHOLD = 5.0  # 单日涨跌幅超过5%视为异动

def fetch_from_finnhub(ticker):
    """从Finnhub获取股票数据"""
    try:
        # 获取实时报价
        quote_url = f"{FINNHUB_BASE_URL}/quote?symbol={ticker}&token={FINNHUB_API_KEY}"
        response = requests.get(quote_url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Finnhub返回数据格式：c=当前价, h=最高, l=最低, o=开盘, pc=前收盘
            if data.get('c', 0) > 0:
                current_price = data['c']
                prev_close = data.get('pc', current_price)
                
                # 计算日涨跌幅
                price_change_1d = ((current_price / prev_close) - 1) * 100 if prev_close > 0 else 0
                
                return {
                    'source': 'finnhub',
                    'current_price': round(current_price, 2),
                    'high': data.get('h', 0),
                    'low': data.get('l', 0),
                    'open': data.get('o', 0),
                    'prev_close': prev_close,
                    'price_change_1d': round(price_change_1d, 2)
                }
        
        return None
    except Exception as e:
        print(f"  Finnhub API错误: {str(e)}")
        return None

def fetch_from_yfinance(ticker):
    """从yfinance获取股票数据（备用）"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        
        if hist.empty:
            return None
        
        current_price = hist['Close'].iloc[-1]
        price_change_1d = ((current_price / hist['Close'].iloc[-2]) - 1) * 100 if len(hist) > 1 else 0
        
        return {
            'source': 'yfinance',
            'current_price': round(current_price, 2),
            'high': hist['High'].iloc[-1],
            'low': hist['Low'].iloc[-1],
            'open': hist['Open'].iloc[-1],
            'prev_close': hist['Close'].iloc[-2] if len(hist) > 1 else current_price,
            'price_change_1d': round(price_change_1d, 2)
        }
    except Exception as e:
        print(f"  yfinance错误: {str(e)}")
        return None

def fetch_abnormal_reason(ticker, price_change):
    """
    收集异动原因分析
    数据源：Finnhub新闻API + yfinance基本面数据
    """
    reasons = []
    
    try:
        # 1. 获取最新新闻（Finnhub）
        news_url = f"{FINNHUB_BASE_URL}/company-news?symbol={ticker}&from={(datetime.now()-timedelta(days=3)).strftime('%Y-%m-%d')}&to={datetime.now().strftime('%Y-%m-%d')}&token={FINNHUB_API_KEY}"
        response = requests.get(news_url, timeout=10)
        
        if response.status_code == 200:
            news_data = response.json()
            
            if news_data and len(news_data) > 0:
                # 只取最新的3条新闻
                top_news = news_data[:3]
                news_headlines = []
                for news in top_news:
                    headline = news.get('headline', '')
                    source = news.get('source', '')
                    if headline:
                        news_headlines.append(f"📰 {headline} ({source})")
                
                if news_headlines:
                    reasons.append("**最新新闻**:\n" + "\n".join(news_headlines))
        
        # 2. 获取基本面数据异动（yfinance）
        stock = yf.Ticker(ticker)
        
        # 检查财报发布
        try:
            earnings = stock.earnings_dates
            if earnings is not None and len(earnings) > 0:
                recent_earnings = earnings.head(1)
                earnings_date = recent_earnings.index[0]
                if (datetime.now() - earnings_date).days <= 5:
                    reasons.append(f"📊 **财报发布**: {earnings_date.strftime('%Y-%m-%d')}")
        except:
            pass
        
        # 检查分析师评级变化
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
        
        # 3. 市场情绪判断
        if price_change > 10:
            reasons.append("🚀 **市场情绪**: 强势拉升，可能受利好催化")
        elif price_change > 5:
            reasons.append("📈 **市场情绪**: 积极上涨，关注持续性")
        elif price_change < -10:
            reasons.append("💔 **市场情绪**: 恐慌性下跌，警惕连锁反应")
        elif price_change < -5:
            reasons.append("📉 **市场情绪**: 显著下跌，注意风险")
        
        # 4. 技术面判断
        hist = stock.history(period="5d")
        if len(hist) >= 2:
            volume_increase = (hist['Volume'].iloc[-1] / hist['Volume'].iloc[-2] - 1) * 100
            if volume_increase > 100:
                reasons.append(f"📊 **成交量异动**: 放量{volume_increase:.0f}%（可能有资金博弈）")
        
    except Exception as e:
        reasons.append(f"⚠️ 原因分析获取失败: {str(e)}")
    
    # 如果没有找到明确原因
    if not reasons:
        if abs(price_change) > 5:
            reasons.append("❓ **暂无明确消息**，建议关注盘后新闻和市场解读")
    
    return "\n".join(reasons) if reasons else "无异动原因"

def fetch_stock_data(ticker, retries=3):
    """获取股票数据，带重试机制和多数据源fallback"""
    for attempt in range(retries):
        try:
            # 1. 优先使用Finnhub API
            print(f"  尝试Finnhub...", end='')
            basic_data = fetch_from_finnhub(ticker)
            
            # 2. Finnhub失败则使用yfinance备用
            if basic_data is None:
                print(f" 失败，切换yfinance...", end='')
                basic_data = fetch_from_yfinance(ticker)
            
            if basic_data is None:
                if attempt < retries - 1:
                    print(f" 重试{attempt+1}/{retries}...")
                    time.sleep(2)
                    continue
                else:
                    print(f" ❌ 所有数据源均失败")
                    return None
            
            print(f" ✅ [{basic_data['source']}]")
            
            # 使用yfinance获取历史数据用于技术指标计算
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo")
            
            if hist.empty:
                print(f"⚠️  {ticker}: 无历史数据")
                return None
            
            current_price = basic_data['current_price']
            
            # 计算ATR (14日)
            high_low = hist['High'] - hist['Low']
            high_close = abs(hist['High'] - hist['Close'].shift())
            low_close = abs(hist['Low'] - hist['Close'].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            atr = tr.rolling(14).mean().iloc[-1]
            
            # 计算RS相对强度（vs SPY）
            try:
                spy = yf.Ticker("SPY").history(period="3mo")
                stock_return = (current_price / hist['Close'].iloc[0] - 1) * 100
                spy_return = (spy['Close'].iloc[-1] / spy['Close'].iloc[0] - 1) * 100
                rs_score = stock_return - spy_return
            except:
                rs_score = 0
            
            # 计算动量指标
            sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            sma_60 = hist['Close'].rolling(60).mean().iloc[-1] if len(hist) >= 60 else sma_20
            
            momentum_score = 0
            if current_price > sma_20 > sma_60:
                momentum_score = 10  # 均线多头排列
            elif current_price > sma_20:
                momentum_score = 5
            elif current_price < sma_20 < sma_60:
                momentum_score = -10  # 均线空头排列
            
            # 计算成交量趋势
            vol_ma_20 = hist['Volume'].rolling(20).mean().iloc[-1]
            current_vol = hist['Volume'].iloc[-1]
            volume_signal = 5 if current_vol > vol_ma_20 * 1.5 else 0
            
            # 获取机构持仓数据
            try:
                institutional_holders = stock.institutional_holders
                if institutional_holders is not None and len(institutional_holders) > 0:
                    institution_score = 10  # 有机构持仓数据
                else:
                    institution_score = 0
            except:
                institution_score = 0
            
            # 获取分析师评级
            try:
                recommendations = stock.recommendations
                if recommendations is not None and len(recommendations) > 0:
                    recent = recommendations.tail(5)
                    buy_count = len(recent[recent['To Grade'].str.contains('Buy|Outperform', case=False, na=False)])
                    analyst_score = min(10, buy_count * 2)
                else:
                    analyst_score = 0
            except:
                analyst_score = 0
            
            # 计算价格变动（优先使用Finnhub实时数据）
            price_change_1d = basic_data['price_change_1d']
            price_change_5d = ((current_price / hist['Close'].iloc[-6]) - 1) * 100 if len(hist) > 5 else 0
            
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
                'data_source': basic_data['source']  # 记录数据源
            }
            
        except Exception as e:
            if attempt < retries - 1:
                print(f"⚠️  {ticker}: 重试 {attempt + 1}/{retries}... ({str(e)})")
                time.sleep(2)
            else:
                print(f"❌ {ticker}: 获取失败 - {str(e)}")
                return None

def calculate_scores(row, market_data):
    """计算2.0评分体系"""
    
    if market_data is None:
        return None
    
    # === 宏观风控 ===
    macro_penalty = 0  # 实际使用时需要接入US10Y数据
    
    # === 技术面 (40分) ===
    rs_score_tech = 0
    if market_data['rs_score'] > 10:
        rs_score_tech = 10
    elif market_data['rs_score'] > 0:
        rs_score_tech = 5
    elif market_data['rs_score'] < -10:
        rs_score_tech = -10
    
    # VAP筹码分布（简化：用成交量信号代替）
    vap_score = market_data['volume_signal']
    
    # 趋势动量
    momentum = market_data['momentum_score']
    
    tech_total = 20 + rs_score_tech + vap_score + momentum
    tech_total = max(0, min(40, tech_total))
    
    # === 资金面 (40分) ===
    institution = market_data['institution_score']
    
    # 筹码集中度（简化）
    chips_score = 5 if market_data['price_change_5d'] > 0 else -5
    
    # 空头博弈潜力（简化）
    short_score = 5
    
    funds_total = 20 + institution + chips_score + short_score
    funds_total = max(0, min(40, funds_total))
    
    # === 消息面 (20分) ===
    catalyst_score = 0  # 需要接入新闻API
    analyst = market_data['analyst_score']
    sentiment = 0  # 需要接入社交媒体情绪
    
    info_total = 10 + catalyst_score + analyst + sentiment
    info_total = max(0, min(20, info_total))
    
    # === 综合评分 ===
    total_score = int((0.4 * tech_total) + (0.4 * funds_total) + (0.2 * info_total) - macro_penalty)
    
    # === 风控计算 ===
    current_price = market_data['current_price']
    atr = market_data['atr']
    
    # 根据分类设置N值
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
    
    # === 价格区间判断 ===
    # 简化判断逻辑，基于RS和momentum
    sma_60 = market_data.get('sma_60', market_data['current_price'])
    if rs_score_tech >= 10 and momentum > 5:
        price_zone = '买入狙击区'
    elif rs_score_tech >= 5 and momentum >= 0:
        price_zone = '加仓确认区'
    elif rs_score_tech < 0 and momentum < 0:
        price_zone = '深度回调区'
    elif market_data['current_price'] > sma_60:
        price_zone = '持仓观察区'
    else:
        price_zone = '待评估'
    
    # === 操盘建议 ===
    if total_score >= 80 and price_zone == '买入狙击区' and rrr >= 2.5:
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

def main():
    print("=" * 80)
    print("🚀 美股投资标的2.0自动更新任务启动")
    print("=" * 80)
    print(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 读取现有数据
    excel_file = '/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx'
    if not os.path.exists(excel_file):
        print(f"❌ 文件不存在: {excel_file}")
        return
    
    df = pd.read_excel(excel_file)
    print(f"📊 读取到 {len(df)} 只股票")
    print()
    
    # 获取所有股票的实时数据
    success_count = 0
    failed_tickers = []
    data_source_stats = {'finnhub': 0, 'yfinance': 0}
    
    results = []
    abnormal_stocks = []  # 记录异动股票
    
    for idx, row in df.iterrows():
        ticker = row['股票代码']
        print(f"[{idx+1}/{len(df)}] 正在获取 {ticker} 数据...", end=' ')
        
        market_data = fetch_stock_data(ticker)
        
        if market_data:
            scores = calculate_scores(row, market_data)
            if scores:
                results.append({
                    'ticker': ticker,
                    'data': market_data,
                    'scores': scores
                })
                success_count += 1
                data_source_stats[market_data['data_source']] += 1
                print(f"✅ ${scores['current_price']} | 评分: {scores['total_score']} | {scores['priority']}")
                
                # 检测异动并收集原因
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
                    time.sleep(1)  # 额外延迟，避免新闻API限流
            else:
                failed_tickers.append(ticker)
                print("❌ 评分计算失败")
        else:
            failed_tickers.append(ticker)
        
        # 避免API限流（Finnhub免费版有限制）
        time.sleep(1.5)
    
    print()
    print("=" * 80)
    print(f"✅ 数据获取完成: {success_count}/{len(df)} 成功")
    if failed_tickers:
        print(f"❌ 失败标的: {', '.join(failed_tickers)}")
    print("=" * 80)
    print()
    
    # 更新DataFrame
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
    
    # 添加更新时间列
    df['最后更新时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 保存更新后的数据
    output_file = '/data/workspace/美股投资标的_跟踪2.0.xlsx'
    df.to_excel(output_file, index=False, engine='openpyxl')
    print(f"💾 数据已保存: {output_file}")
    print()
    
    # 生成分析报告
    a_grade = df[df['执行优先级'] == 'A级'].sort_values('总评分', ascending=False) if '执行优先级' in df.columns else pd.DataFrame()
    b_grade = df[df['执行优先级'] == 'B级'].sort_values('总评分', ascending=False) if '执行优先级' in df.columns else pd.DataFrame()
    
    # 找出价格异动标的
    price_movers = []
    for result in results:
        if abs(float(result['scores']['price_change_1d'].replace('%', '').replace('+', ''))) > 5:
            price_movers.append({
                'ticker': result['ticker'],
                'change': result['scores']['price_change_1d']
            })
    
    report = f"""
📊 **美股投资标的2.0更新报告**
⏰ 更新时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

### 📈 更新概况
- 成功更新: {success_count}/{len(df)} 只 ({success_count/len(df)*100:.1f}%)
- 失败标的: {len(failed_tickers)} 只
- 数据源: Finnhub {data_source_stats['finnhub']}只 | yfinance {data_source_stats['yfinance']}只

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
    
    # 添加异动原因详细分析
    if abnormal_stocks:
        report += "\n### 🔍 异动原因深度分析\n"
        report += f"*共检测到 {len(abnormal_stocks)} 只异动标的*\n\n"
        
        # 按涨跌幅排序
        abnormal_stocks.sort(key=lambda x: abs(x['change']), reverse=True)
        
        for idx, stock in enumerate(abnormal_stocks[:8], 1):  # 最多展示8只
            emoji = "📈" if stock['change'] > 0 else "📉"
            report += f"#### {idx}. {emoji} **{stock['ticker']}** - {stock['name']} ({stock['category']})\n"
            report += f"- **价格**: ${stock['price']} | **涨跌**: {stock['change']:+.2f}% | **评分**: {stock['score']}分 | **优先级**: {stock['priority']}\n"
            report += f"- **异动原因**:\n{stock['reason']}\n\n"
    
    if failed_tickers:
        report += f"\n### ⚠️ 更新失败标的\n{', '.join(failed_tickers)}\n"
    
    report += "\n---\n*数据源: Finnhub API (主) + Yahoo Finance (备用) | 分析框架: 专业作手2.0体系*"
    
    print(report)
    
    # 保存报告
    report_file = f'/data/workspace/美股2.0更新报告_{datetime.now().strftime("%Y%m%d_%H%M")}.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 报告已保存: {report_file}")
    print("=" * 80)
    
    # === 集成Finance-Manager深度财务分析 ===
    try:
        print("\n" + "=" * 80)
        print("📊 Finance-Manager 深度财务分析启动...")
        print("=" * 80)
        
        # 导入财务分析模块
        import sys
        sys.path.append('/data/workspace/scripts')
        from finance_analysis_integration import (
            analyze_portfolio_financials,
            generate_html_report,
            generate_wechat_notification
        )
        
        # 执行财务分析
        analysis = analyze_portfolio_financials(excel_file)
        
        # 生成HTML可视化报告
        html_report_path = f'/data/workspace/美股财务分析报告_{datetime.now().strftime("%Y%m%d_%H%M")}.html'
        generate_html_report(analysis, html_report_path)
        print(f"✅ HTML报告已生成: {html_report_path}")
        
        # 保存JSON数据
        json_path = f'/data/workspace/美股财务分析数据_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON数据已保存: {json_path}")
        
        # 生成增强的企业微信通知
        wechat_notification = generate_wechat_notification(analysis)
        
        # 合并原有报告和财务分析
        enhanced_report = report + "\n\n" + "=" * 80 + "\n" + wechat_notification
        
        print("\n" + "=" * 80)
        print("✅ Finance-Manager分析完成！")
        print("=" * 80)
        
        return enhanced_report
        
    except Exception as e:
        print(f"⚠️ Finance-Manager分析出错: {str(e)}")
        print("继续使用原始报告...")
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
        print("[REPORT_FOR_NOTIFY]")
        print(error_msg)
        sys.exit(1)
