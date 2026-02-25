#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯yfinance模式测试脚本 - 跳过富途测试
测试yfinance获取股票数据和指数数据的能力
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import sys

def test_yfinance():
    """测试yfinance获取单只股票"""
    print("\n" + "="*60)
    print("测试1: yfinance 单只股票数据获取")
    print("="*60)
    
    try:
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        
        if not hist.empty:
            latest = hist.iloc[-1]
            print(f"✅ 测试通过 | AAPL")
            print(f"   最新价格: ${latest['Close']:.2f}")
            print(f"   成交量: {latest['Volume']:,.0f}")
            print(f"   数据日期: {hist.index[-1].strftime('%Y-%m-%d')}")
            return True
        else:
            print(f"❌ 测试失败 | AAPL: 无历史数据")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败 | AAPL: {str(e)}")
        return False

def test_batch_stocks():
    """测试批量获取股票数据"""
    print("\n" + "="*60)
    print("测试2: yfinance 批量股票数据获取")
    print("="*60)
    
    test_symbols = ["USAR", "MP", "CCJ", "NVDA", "GOOG"]
    
    try:
        success_count = 0
        fail_list = []
        
        for symbol in test_symbols:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="5d")
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    print(f"✅ {symbol:6s} | ${latest['Close']:8.2f} | Vol: {latest['Volume']:>12,.0f}")
                    success_count += 1
                else:
                    print(f"❌ {symbol:6s} | 无数据")
                    fail_list.append(symbol)
                    
            except Exception as e:
                print(f"❌ {symbol:6s} | 错误: {str(e)[:40]}")
                fail_list.append(symbol)
        
        success_rate = (success_count / len(test_symbols)) * 100
        print(f"\n成功率: {success_rate:.1f}% ({success_count}/{len(test_symbols)})")
        
        if fail_list:
            print(f"失败标的: {', '.join(fail_list)}")
        
        return success_rate >= 80.0
        
    except Exception as e:
        print(f"❌ 批量测试失败: {str(e)}")
        return False

def test_index_data():
    """测试指数数据获取 (QQQ, SPY)"""
    print("\n" + "="*60)
    print("测试3: 指数数据获取 (QQQ & SPY)")
    print("="*60)
    
    try:
        for symbol in ["QQQ", "SPY"]:
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="50d")
                
                if len(hist) >= 20:
                    latest = hist.iloc[-1]
                    
                    # 计算技术指标
                    close_prices = hist['Close']
                    ma20 = close_prices.rolling(window=20).mean().iloc[-1]
                    ma50 = close_prices.rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
                    
                    # 判断趋势
                    trend = "多头" if latest['Close'] > ma20 else "空头"
                    
                    print(f"✅ {symbol} | ${latest['Close']:.2f}")
                    print(f"   MA20: ${ma20:.2f} | 趋势: {trend}")
                    if ma50:
                        print(f"   MA50: ${ma50:.2f}")
                else:
                    print(f"❌ {symbol} | 数据不足 (仅{len(hist)}天)")
                    return False
                    
            except Exception as e:
                print(f"❌ {symbol} | 错误: {str(e)}")
                return False
        
        print("\n✅ 指数数据测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 指数测试失败: {str(e)}")
        return False

def test_excel_access():
    """测试Excel文件访问"""
    print("\n" + "="*60)
    print("测试4: Excel文件访问")
    print("="*60)
    
    excel_path = "/data/workspace/stock_pool/美股投资标的_跟踪2.0.xlsx"
    
    try:
        df = pd.read_excel(excel_path, sheet_name="Sheet1")
        
        if not df.empty:
            symbol_col = None
            for col in df.columns:
                if '代码' in str(col) or 'Symbol' in str(col) or 'symbol' in str(col):
                    symbol_col = col
                    break
            
            if symbol_col:
                symbols = df[symbol_col].dropna().tolist()
                print(f"✅ Excel文件读取成功")
                print(f"   文件路径: {excel_path}")
                print(f"   标的数量: {len(symbols)}")
                print(f"   前5个标的: {', '.join([str(s) for s in symbols[:5]])}")
                return True
            else:
                print(f"❌ 未找到股票代码列")
                return False
        else:
            print(f"❌ Excel文件为空")
            return False
            
    except Exception as e:
        print(f"❌ Excel文件读取失败: {str(e)}")
        return False

def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("🚀 纯yfinance模式测试 - V4系统")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试环境: AnyDev开发机 (无富途OpenD)")
    
    results = {
        "yfinance单只": test_yfinance(),
        "yfinance批量": test_batch_stocks(),
        "指数数据": test_index_data(),
        "Excel文件": test_excel_access()
    }
    
    # 汇总结果
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} | {test_name}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n总体通过率: {(passed/total)*100:.0f}% ({passed}/{total})")
    
    if passed == total:
        print("\n🎉 所有测试通过！V4系统可以正常运行（纯yfinance模式）")
        print("\n📝 下一步操作：")
        print("   1. 运行完整更新: python3 /data/workspace/scripts/update_stock_2.0_v4.py")
        print("   2. 查看更新报告: ls -lt /data/workspace/美股2.0更新报告_*.md | head -1")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查网络连接和依赖库")
        return 1

if __name__ == "__main__":
    sys.exit(main())
