import React, { Fragment } from 'react'
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
  } from 'chart.js';
import { Bar } from 'react-chartjs-2';

const BarGraph = (props) => {
    ChartJS.register(
        CategoryScale,
        LinearScale,
        BarElement,
        Title,
        Tooltip,
        Legend
    );

    const options = {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Sentiment Graph',
          },
        },
    };

    const labels = ['negative', 'neutral', 'positive'];

    const data = {
        labels,
        datasets: [
            {
                label: 'compound score',
                data: props.data,
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
            },
        ],
    };
  return (
    <Fragment>
        <Bar options={options} data={data} />
    </Fragment>
  )
}

export default BarGraph