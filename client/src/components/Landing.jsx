import React, { Fragment, useState } from 'react'
import '../styles/css/landing.css'
import { ReactComponent as Send } from '../assets/svg/arrow-up-right-from-square.svg'
import axios from 'axios'
import BarGraph from './BarGraph'
import { getJwtToken, getRefreshToken } from '../includes/session'

const Landing = () => {
    const [checkt, setCheckt] = useState({
        mtweet: ''
    })
    const [response, setResponse] = useState({data: [], message: '', type: '', hate:{result:''}, 'analysis':{'state':false,'compound':0}})
    const [analyze, setAnalyze] = useState({state:false, text:'check'})
    const subfrom = (e) => {
        e.preventDefault()
        setAnalyze({state:true, text:'analyzing'})
        check('', false)
        setCheckt({mtweet: ''})
    }
    const [gt, setGt] = useState({state: false, btn:'get tweets'})
    const twitter = async () => {
        // set btn animation
        setGt({state: true, btn:'fetching'})
        let config = {
          method: 'post',
          url: 'http://localhost:5000/twitter',
          headers: { 
            'Content-Type': 'application/json'
          },
          data : JSON.stringify({keyword: ''})
        };
        try{
            let res = await axios(config)
            setResponse({data: res.data.data, hate:{result:''}, analysis:{state:false}})
            setCheckt({mtweet: ''})
            setGt({state: false, btn:'get tweets'})
        } catch(err) {
            console.log(err)
        }
    }
    const check = async (t, r) => {
        if(t===undefined || t===''){
            t = checkt.mtweet
        }
        let config = {
          method: 'post',
          url: 'http://localhost:5000/check',
          headers: { 
            'Content-Type': 'application/json'
          },
          data : JSON.stringify({mtweet: t, twitterpull: r, token:{jwt: getJwtToken(), refreshToken:getRefreshToken()}})
        };
        try{
            let res = await axios(config)
            setResponse(res.data)
            setCheckt({mtweet: ''})
            setAnalyze({state:false, text:'check'})
        } catch(err) {
            console.log(err)
        }
    }
    const clean = (t) => {
        let expression = /(#[a-z0-9_]+)|((https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}))|(([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD10-\uDDFF]))/gi
        let regex = new RegExp(expression)
        let twt = t.replace(regex,'').replace(/\s+/g, ' ').trim()
        let remmentions = /(^|)(@[a-zA-Z0-9_\d-]+)/gi
        return twt.replace(remmentions, '').trim()
    }
    const [opdeck, setOpdeck] = useState('manual')
    console.log(response);
  return (
    <Fragment>
        <div className="infotxts">
            <h1 className="about-title">Twitter hate crime and cyberbullying detection</h1>
            <p className="creator">Created by <a href="https://github.com/scientiaChela" rel="noopener noreferrer" target="_blank">Cynthia Chelang'at<Send className="sendicon"/></a> and <a href="https://github.com/DennisRono" rel="noopener noreferrer" target="_blank">Dennis Kibet<Send className="sendicon"/></a></p>
            <p className="abt-cont">The widespread usage of social media, blogging, and other social communication services has been more apparent in recent years. Users of these services are exposed to content made by other people. The majority of the time, that content may include derogatory or abusive language that could target or insult particular user groups without offering helpful information.</p>
            <p className="abt-cont">Hate speech is defined as "abusive speech targeting specific group characteristics, such as ethnicity, religion, or gender".</p>
            <p className="abt-cont">If not restrained, this language usage could make such services less appealing to the average user, particularly in social networks and product review websites, it may even cause uproar and fights on sensitive subject like election. <br/>
            In order to enhance user experience and uphold the reputation of the business involved, screening this kind of content becomes essential. In addition, the volume of data generated by these services is too large for human resources to process. A useful tool would be automatic software that could recognize such offensive words.
            This classifier is trained to distinguish between the categories of "Hate Speech" and "Non Hate Speech" in texts.</p>
        </div>
        <div className="choicedeck">
            <button className={(opdeck==='twitter')?"gettwittertweets":"gettwittertweets hidecab"} onClick={()=>{setOpdeck('manual')}}>Type your own tweets</button>
            <button className={(opdeck==='manual')?"gettwittertweets":"gettwittertweets hidecab"} onClick={()=>{setOpdeck('twitter')}}>twitter</button>
        </div>
        <div className="landing">
            <div className={(opdeck==='twitter')?"manualtweet hidecab":"manualtweet"}>
                <h2 className="landingtitle">Is Your Tweet Considered Hate Speech?</h2>
                <p className="landingtexts">Please note that this prediction is based on how the model was trained, so it may not be an <br /> accurate representation.</p>
                <form className="landingform" onSubmit={(e)=>{subfrom(e)}}>
                    {(response.message!=='')?<p className={(response.type==='success')?"formNotifySucc":"formNotify"}>{response.message}</p>:null}
                    <div className="form-group">
                        <label htmlFor="tweet">Enter tweet</label><br />
                        <input type="text" className="landingtweetinput" name="mtweet" value={checkt.mtweet} onChange={(e)=>{setCheckt({ ...checkt, [e.target.name]: e.target.value })}} required/>
                    </div>
                    <button type="submit" className={(analyze.state)?"lsubmitBtn rainbow":"lsubmitBtn"}>{analyze.text}</button>
                </form>
            </div>
            <div className={(opdeck==='manual')?"getfromtwitter hidecab":"getfromtwitter"}>
                <h2 className="landingtitle">Get Random tweets by keyword from twitter?</h2>
                <p className="landingtexts">Please note that this prediction is based on how the model was trained, so it may not be an <br /> accurate representation.</p>
                {/* <form className="landingform" onSubmit={(e)=>{subkeyword(e)}}>
                    {(response.message!=='')?<p className={(response.type==='success')?"formNotifySucc":"formNotify"}>{response.message}</p>:null}
                    <div className="form-group">
                        <label htmlFor="tweet">Enter keyword</label><br />
                        <input type="text" className="landingtweetinput" name="mtweet" value={keyword} onChange={(e)=>{setKeyword(e.target.value)}} required/>
                    </div>
                    <button type="submit" className={(gt.state)?"gettwittertweets rainbow":"gettwittertweets"} >{gt.btn}</button>
                </form> */}
                <button className={(gt.state)?"gettwittertweets rainbow":"gettwittertweets"} onClick={()=>{twitter()}}>{gt.btn}</button>
                <div className="fetchedtweets">
                    {(response.hate.result !== undefined)?
                        (response.data.length !== 0 && response.tpull !== true)?
                            <div className="table-wrap">
                                <table>
                                    <thead>
                                    <tr>
                                        <td className="tdHeader">Tweet</td>
                                        <td className="tdHeader"><center>check</center></td>
                                    </tr>
                                    </thead>
                                    <tbody>
                                        {response.data.map(item=> {
                                            return (
                                            <tr key={item.id}>
                                                <td>{clean(item.text)}</td>
                                                <td><button className="gettwittertweets" onClick={()=>{check(item.text, true); }}>select</button></td>
                                            </tr>
                                            )
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        :null
                    :null}
                </div>
            </div>
            <div className="results">
                {(response.hate.result !== undefined)?
                    (response.hate.result !== '')?
                        <div className={(response.hate.hate==='true')?"resplay hate":"resplay"}>
                            <h3>{response.hate.result}</h3>
                        </div>
                    :null
                :null}
                {(response.analysis.state !== undefined)?
                    (response.analysis.state==='true')?
                        <div className="sentimentbox">
                            <h2>Sentiment Analysis with VADER</h2>
                            <p>VADER is a lexicon designed for scoring social media.</p>
                            <div className="sentimentflex">
                                <div className="sentTexts">
                                    <p>Your Tweet is rated as {response.analysis.status}</p>
                                    <p>Compound Score: {response.analysis.dictionary.compound}</p>
                                    <p>Polarity Breakdown:</p>
                                    <p>{response.analysis.dictionary.neg * 100} % Negative</p>
                                    <p>{response.analysis.dictionary.neu * 100} % Neutral</p>
                                    <p>{response.analysis.dictionary.pos * 100} % Positive</p>
                                </div>
                                <div className="sentGraphs">
                                    <BarGraph data={[response.analysis.dictionary.neg, response.analysis.dictionary.neu, response.analysis.dictionary.pos]}/>
                                </div>
                            </div>
                        </div>
                    :null
                :null}
            </div>
        </div>
    </Fragment>
  )
}

export default Landing