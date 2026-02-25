#!/usr/bin/env python3
"""
美股投资标的2.0 V4 - 快速测试脚本
测试各个数据源和指数功能
"""

import sys
import time

def test_futu():
    """测试富途OpenAPI连接"""
    print("\n" + "=" * 60)
    print("测试1: 富途OpenAPI")
    print("=" * 60)
    
    try:
        from futu import OpenQuoteContext, RET_OK
        
        print("尝试连接富途OpenD (127.0.0.1:11111)...")
        quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
        
        print("获取AAPL报价...")
        ret, data = quote_ctx.get_market_snapshot(['US.AAPL'])
        
        if ret == RET_OK and not data.empty:
            price = data.iloc[0]['last_price']
            print(f"✅ 富途连接成功!")
            print(f"   AAPL价格: ${price:.2f}")
            quote_ctx.close()
            return True
        else:
            print(f"❌ 富途API返回错误: {data}")
            quote_ctx.close()
            return False
            
    except ImportError:
        print("⚠️  futu-api未安装")
        print("   安装: pip install futu-api")
        return False
    except Exception as e:
        print(f"❌ 富途连接失败: {str(e)}")
        print("   提示: 确保FutuOpenD已启动")
        return False

def test_yfinance():
    """测试yfinance优化版"""
    print("\n" + "=" * 60)
    print("测试2: yfinance优化版")
    print("=" * 60)
    
    try:
        import yfinance as yf
        import requests
        
        # 创建Session
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        
        print("获取AAPL数据 (60秒超时)...")
        stock = yf.Ticker("AAPL", session=session)
        hist = stock.history(period="5d", timeout=60)
        
        if not hist.empty:
            price = hist['Close'].iloc[-1]
            print(f"✅ yfinance成功!")
            print(f"   AAPL价格: ${price:.2f}")
            return True
        else:
            print("❌ yfinance返回空数据")
            return False
            
    except ImportError:
        print("❌ yfinance未安装")
        print("   安装: pip install yfinance")
        return False
    except Exception as e:
        print(f"❌ yfinance失败: {str(e)}")
        return False

def test_polygon():
    """测试Polygon.io (可选)"""
    print("\n" + "=" * 60)
    print("测试3: Polygon.io (可选)")
    print("=" * 60)
    
    # 检查是否配置了API Key
    POLYGON_API_KEY = "YOUR_POLYGON_API_KEY"  # 从脚本中读取
    
    if POLYGON_API_KEY == "YOUR_POLYGON_API_KEY":
        print("⚠️  Polygon.io API Key未配置")
        print("   如需历史回测功能,请配置API Key")
        print("   注册: https://polygon.io/")
        return None
    
    try:
        import requests
        from datetime import datetime, timedelta
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        url = f"https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/{start_date}/{end_date}"
        params = {
            'adjusted': 'true',
            'apiKey': POLYGON_API_KEY
        }
        
        print(f"获取AAPL历史数据 ({start_date} ~ {end_date})...")
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                count = len(data.get('results', []))
                print(f"✅ Polygon.io成功!")
                print(f"   获取到 {count} 天历史数据")
                return True
        
        print(f"❌ Polygon.io失败: {response.status_code}")
        return False
        
    except Exception as e:
        print(f"❌ Polygon.io错误: {str(e)}")
        return False

def test_index_data():
    """测试指数数据获取"""
    print("\n" + "=" * 60)
    print("测试4: 指数数据获取 (QQQ, SPY)")
    print("=" * 60)
    
    try:
        import yfinance as yf
        import pandas as pd
        
        results = {}
        
        for ticker in ['QQQ', 'SPY']:
            print(f"\n获取 {ticker} 数据...")
            
            stock = yf.Ticker(ticker)
            hist = stock.history(period="3mo", timeout=60)
            
            if hist.empty:
                print(f"❌ {ticker}: 数据为空")
                results[ticker] = None
                continue
            
            current_price = hist['Close'].iloc[-1]
            sma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            sma_60 = hist['Close'].rolling(60).mean().iloc[-1] if len(hist) >= 60 else sma_20
            
            # 趋势判断
            if current_price > sma_20 > sma_60:
                trend = "多头排列"
                signal = 1.0
            elif current_price > sma_20:
                trend = "震荡偏多"
                signal = 0.5
            elif current_price < sma_20 < sma_60:
                trend = "空头排列"
                signal = -1.0
            else:
                trend = "震荡"
                signal = 0
            
            results[ticker] = {
                'price': current_price,
                'trend': trend,
                'signal': signal
            }
            
            print(f"✅ {ticker}: ${current_price:.2f} | {trend} (信号: {signal:+.1f})")
        
        # 市场环境判断
        if results['QQQ'] and results['SPY']:
            avg_signal = (results['QQQ']['signal'] + results['SPY']['signal']) / 2
            
            print(f"\n📊 市场环境判断:")
            print(f"   平均信号: {avg_signal:+.2f}")
            
            if avg_signal >= 0.75:
                env = "🟢 强势多头,适合积极做多"
            elif avg_signal >= 0:
                env = "🟡 偏多环境,谨慎做多"
            elif avg_signal >= -0.5:
                env = "🟠 震荡市,控制仓位"
            else:
                env = "🔴 弱势空头,避免做多"
            
            print(f"   {env}")
            return True
        else:
            print("\n❌ 指数数据获取不完整")
            return False
        
    except Exception as e:
        print(f"❌ 指数数据测试失败: {str(e)}")
        return False

def test_excel_file():
    """测试Excel文件完整性"""
    print("\n" + "=" * 60)
    print("测试5: Excel文件完整性")
    print("=" * 60)
    
    try:
        import pandas as pd
        
        excel_file = '/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx'
        
        print(f"读取: {excel_file}")
        df = pd.read_excel(excel_file)
        
        print(f"✅ 总标的数: {len(df)}")
        
        # 检查指数标的
        tickers = df['股票代码'].tolist()
        
        if 'QQQ' in tickers and 'SPY' in tickers:
            print("✅ 指数标的完整 (QQQ, SPY)")
        else:
            print("⚠️  缺少指数标的")
            print("   运行: python /data/workspace/scripts/add_index_tickers.py")
        
        # 检查必要列
        required_cols = ['分类', '股票代码', '总评分', '执行优先级', '操盘建议']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if not missing_cols:
            print("✅ 必要列完整")
        else:
            print(f"❌ 缺少列: {missing_cols}")
            return False
        
        # 显示统计
        print(f"\n📊 标的分类:")
        if '分类' in df.columns:
            for category, count in df['分类'].value_counts().items():
                print(f"   {category}: {count}只")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Excel文件不存在: {excel_file}")
        return False
    except Exception as e:
        print(f"❌ Excel测试失败: {str(e)}")
        return False

def main():
    print("\n" + "=" * 60)
    print("🧪 美股投资标的2.0 V4 - 功能测试")
    print("=" * 60)
    
    results = {
        '富途OpenAPI': test_futu(),
        'yfinance优化版': test_yfinance(),
        'Polygon.io': test_polygon(),
        '指数数据': test_index_data(),
        'Excel文件': test_excel_file(),
    }
    
    # 测试总结
    print("\n" + "=" * 60)
    print("📋 测试总结")
    print("=" * 60)
    
    for name, result in results.items():
        if result is True:
            status = "✅ 通过"
        elif result is False:
            status = "❌ 失败"
        else:
            status = "⚠️  跳过"
        
        print(f"{status} | {name}")
    
    # 最终建议
    print("\n" + "=" * 60)
    print("💡 建议")
    print("=" * 60)
    
    if results['富途OpenAPI']:
        print("✅ 富途可用,将作为主数据源")
    else:
        print("⚠️  富途不可用,将使用yfinance备用源")
    
    if results['yfinance优化版']:
        print("✅ yfinance可用,作为备用数据源")
    else:
        print("❌ yfinance不可用,可能影响数据获取")
    
    if results['指数数据']:
        print("✅ 指数数据可用,支持市场环境判断")
    else:
        print("⚠️  指数数据不可用,将缺少市场环境判断")
    
    if results['Excel文件']:
        print("✅ Excel文件完整,可以开始更新")
    else:
        print("❌ Excel文件有问题,请先修复")
    
    # 判断是否可以运行
    print("\n" + "=" * 60)
    
    if results['yfinance优化版'] and results['Excel文件']:
        print("🚀 系统就绪,可以运行V4脚本")
        print("   运行: python /data/workspace/scripts/update_stock_2.0_v4.py")
    else:
        print("⚠️  系统未就绪,请先解决上述问题")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
