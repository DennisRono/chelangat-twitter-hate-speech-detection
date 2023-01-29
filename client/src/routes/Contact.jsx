import React, { Fragment, useState } from 'react'
import '../styles/css/auth.css'
import Header from '../components/Header'
import { Helmet } from "react-helmet"
import axios from 'axios'

const Contact = () => {
  const [conatct, setConatct] = useState({
    fname: '',
    lname: '',
    email: '',
    brief: ''
  })
  const [response, setResponse] = useState({data: [], message: '', type: ''})
  const contactme = async (e) => {
    e.preventDefault()
    let config = {
        method: 'post',
        url: 'http://localhost:5000/contact',
        headers: { 
          'Content-Type': 'application/json'
        },
        data : JSON.stringify(conatct)
    };
    try{
        let res = await axios(config)
        setResponse(res.data)
        setConatct({
            fname: '',
            lname: '',
            email: '',
            brief: ''
        })
        setTimeout(() => {
            setResponse({data: [], message: '', type: ''})
        }, 2000);
    } catch(err) {
        console.log(err)
    }
  }
  return (
    <Fragment>
      <Helmet>
          <meta charSet="utf-8" />
          <title>Contact Us | Twitter Hate Speech Detection</title>
      </Helmet>
      <Header/>
        <div className="authentification">
          <section className="contact">
            <div className="contact-wrapper">
                <div className="contFormSec">
                    <h2 className="contact-header">Contact Me</h2>
                    {(response.message!=='')?<p className={(response.type==='success')?"formNotifySucc":"formNotify"}>{response.message}</p>:null}
                    <form className="registration-form" onSubmit={(e)=>{contactme(e)}}>
                        <div className="cont-group">
                            <div className="cont-gr-flex">
                                <div className="contPut">
                                    <div className="user-input-wrp">
                                        <br/>
                                        <input id="id-input" type="text" className="inputText" name="fname" value={conatct.fname} onChange={(e)=>{setConatct({ ...conatct, [e.target.name]: e.target.value })}} required/>
                                        <span className="floating-label">First Name <span style={{color: "red"}}>*</span></span>
                                    </div>
                                    <span id="id-err"></span>
                                </div>
                                <div className="contPut">
                                    <div className="user-input-wrp">
                                        <br/>
                                        <input id="id-input" type="text" className="inputText" name="lname" value={conatct.lname} onChange={(e)=>{setConatct({ ...conatct, [e.target.name]: e.target.value })}} required/>
                                        <span className="floating-label">Last Name <span style={{color: "red"}}>*</span></span>
                                    </div>
                                    <span id="id-err"></span>
                                </div>
                            </div>
                            <div className="user-input-wrp">
                                <br/>
                                <input id="id-input" type="text" className="inputText" name="email" value={conatct.email} onChange={(e)=>{setConatct({ ...conatct, [e.target.name]: e.target.value })}} required/>
                                <span className="floating-label">Email Address <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                            <br/>
                            <div className="user-input-wrp">
                                <br/>
                                <textarea id="id-input" type="text" onkeyup="this.setAttribute('value', this.value);" className="inputText" name="brief" value={conatct.brief} onChange={e=>{setConatct({ ...conatct, [e.target.name]: e.target.value })}} style={{minHeight: "100px"}} required></textarea>
                                <span className="floating-label">Type in your message <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <div className="resetting-pass">
                            <input type="submit" value="contact" name="contact" className="contact-btn"/>
                        </div>
                    </form>
                </div>
            </div>
          </section>
        </div>
    </Fragment>
  )
}

export default Contact