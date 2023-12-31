import { months } from '../../data';
import { echartSetOption, tooltipFormatter } from './echarts-utils';

/* -------------------------------------------------------------------------- */
/*                     Echart Bar Member info                                 */
/* -------------------------------------------------------------------------- */
const { echarts } = window;

const returningCustomerChartInit = () => {
  const { getColor, getData } = window.phoenix.utils;

  const $returningCustomerChart = document.querySelector(
    '.echart-returning-customer'
  );

  if ($returningCustomerChart) {
    const userOptions = getData($returningCustomerChart, 'echarts');
    const chart = echarts.init($returningCustomerChart);
    const getDefaultOptions = () => ({
      color: getColor('gray-100'),
      legend: {
        data: [
          {
            name: 'Fourth time',
            icon: 'roundRect',
            itemStyle: {
              color: getColor('primary-300'),
              borderWidth: 0
            }
          },
          {
            name: 'Third time',
            icon: 'roundRect',
            itemStyle: { color: getColor('info-200'), borderWidth: 0 }
          },
          {
            name: 'Second time',
            icon: 'roundRect',
            itemStyle: { color: getColor('primary'), borderWidth: 0 }
          }
        ],

        right: 'right',
        width: '100%',
        itemWidth: 16,
        itemHeight: 8,
        itemGap: 20,
        top: 3,
        inactiveColor: getColor('gray-500'),
        inactiveBorderWidth: 0,
        textStyle: {
          color: getColor('gray-900'),
          fontWeight: 600,
          fontFamily: 'Nunito Sans'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'none'
        },
        padding: [7, 10],
        backgroundColor: getColor('gray-100'),
        borderColor: getColor('gray-300'),
        textStyle: { color: getColor('dark') },
        borderWidth: 1,
        transitionDuration: 0,
        formatter: tooltipFormatter
      },
      xAxis: {
        type: 'category',
        data: months,
        show: true,
        boundaryGap: false,
        axisLine: {
          show: true,
          lineStyle: { color: getColor('gray-300') }
        },
        axisTick: {
          show: false
        },
        axisLabel: {
          // interval: 1,
          showMinLabel: false,
          showMaxLabel: false,
          color: getColor('gray-800'),
          formatter: value => value.slice(0, 3),
          fontFamily: 'Nunito Sans',
          fontWeight: 600,
          fontSize: 12.8
        },
        splitLine: {
          show: true,
          lineStyle: { color: getColor('gray-200'), type: 'dashed' }
        }
      },
      yAxis: {
        type: 'value',
        boundaryGap: false,
        axisLabel: {
          showMinLabel: true,
          showMaxLabel: true,
          color: getColor('gray-800'),
          formatter: value => `${value}%`,
          fontFamily: 'Nunito Sans',
          fontWeight: 600,
          fontSize: 12.8
        },
        splitLine: {
          show: true,
          lineStyle: { color: getColor('gray-200') }
        }
      },
      series: [
        {
          name: 'Fourth time',
          type: 'line',
          data: [62, 90, 90, 90, 78, 84, 17, 17, 17, 17, 82, 95],
          showSymbol: false,
          symbol: 'circle',
          symbolSize: 10,
          emphasis: {
            lineStyle: {
              width: 1
            }
          },
          lineStyle: {
            type: 'dashed',
            width: 1,
            color: getColor('primary-300')
          },
          itemStyle: {
            borderColor: getColor('primary-300'),
            borderWidth: 3
          }
        },
        {
          name: 'Third time',
          type: 'line',
          data: [50, 50, 30, 62, 18, 70, 70, 22, 70, 70, 70, 70],
          showSymbol: false,
          symbol: 'circle',
          symbolSize: 10,
          emphasis: {
            lineStyle: {
              width: 1
            }
          },
          lineStyle: {
            width: 1,
            color: getColor('info-200')
          },
          itemStyle: {
            borderColor: getColor('info-200'),
            borderWidth: 3
          }
        },
        {
          name: 'Second time',
          type: 'line',
          data: [40, 78, 60, 78, 60, 20, 60, 40, 60, 40, 20, 78],
          showSymbol: false,
          symbol: 'circle',
          symbolSize: 10,
          emphasis: {
            lineStyle: {
              width: 3
            }
          },
          lineStyle: {
            width: 3,
            color: getColor('primary')
          },
          itemStyle: {
            borderColor: getColor('primary'),
            borderWidth: 3
          }
        }
      ],
      grid: { left: 0, right: 8, top: '14%', bottom: 0, containLabel: true }
    });
    echartSetOption(chart, userOptions, getDefaultOptions);
  }
};

export default returningCustomerChartInit;
