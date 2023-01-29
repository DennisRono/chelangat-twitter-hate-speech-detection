import React, { Fragment, useState, useEffect } from 'react'
import '../styles/css/history.css'
import Header from '../components/Header'
import { Helmet } from "react-helmet"
import Footer from '../components/Footer'
import axios from 'axios'
import { getJwtToken, getRefreshToken } from '../includes/session'

const History = (props) => {
    const [isLogged, setIsLogged] = useState(props.isLogged)
    // check is user is logged in
    const jwtToken = getJwtToken()
    const refTok = getRefreshToken()
    useEffect(()=>{
      if (!jwtToken && !refTok) {
        setIsLogged(false)
      } else {
        setIsLogged(true)
      }
    },[])

    const [response, setResponse] = useState({data: []})

    const getHistory = async () => {
        let config = {
            method: 'post',
            url: 'http://localhost:5000/history',
            headers: { 
              'Content-Type': 'application/json'
            },
            data : JSON.stringify({token: {jwt:getJwtToken(), refreshToken:getRefreshToken()}})
        };
        try{
            let res = await axios(config)
            setResponse({data:res.data})
        } catch(err) {
              console.log(err)
        }
    }
    useEffect(()=>{
        getHistory()
    },[])
  return (
    <Fragment>
        <Helmet>
            <meta charSet="utf-8" />
            <title>History | Twitter Hate Speech Detection</title>
        </Helmet>
        <Header/>
        <div className="myhistory">
        {(isLogged)?
            <table>
                <thead>
                    <tr>
                        <th>Tweet</th>
                        <th>Result</th>
                        <th>CompoundScore</th>
                        <th>Negative</th>
                        <th>Neutral</th>
                        <th>Positive</th>
                    </tr>
                </thead>

                <tbody>
                    {(response.data.lenght!==0)?
                            response.data.map(item=>{
                                return(
                                <tr>
                                    <td>{item.Tweet}</td>
                                    <td>{item.Result}</td>
                                    <td>{item.CompoundCore}</td>
                                    <td>{item.Negative}</td>
                                    <td>{item.Neutral}</td>
                                    <td>{item.Positive}</td>
                                </tr>
                            )
                        })
                    :null}
                </tbody>
            </table>
        :
            <div className="historynotlogged">
                <h2>Please Login to view history</h2>
            </div>
        }
        </div>
        <Footer/>
    </Fragment>
  )
}

export default History