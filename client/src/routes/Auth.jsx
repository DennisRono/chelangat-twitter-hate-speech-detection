import React, { Fragment, useState } from 'react'
import '../styles/css/auth.css'
import { useNavigate, useLocation } from "react-router-dom"
import useLocalStorage from 'use-local-storage'
import {ReactComponent as Home} from '../assets/svg/home.svg'
import { api } from '../api/axios'
import { Link } from "react-router-dom"
import { setJwtToken, setRefreshToken } from '../includes/session'
import { useEffect } from 'react'


const Auth = () => {
    const [active, setActive] = useLocalStorage('activity', 'login')
    const location = useLocation()
    useEffect(()=>{
        setActive(location.state)
    }, [location.state, setActive])
    const [register, setRegister] = useState({
        fname: '',
        lname: '',
        email: '',
        password: '',
        cpassword: ''
    })
    const [reset, setReset] = useState({
        email: '',
        otp: '',
        password: '',
        cpassword: ''
    })
    const [login, setLogin] = useState({
        email: '',
        password: ''
    })

    const [response, setResponse] = useState({message: '', type: ''})
    const registerSubmit = async (e) => {
        e.preventDefault()
        let res = await api('POST', 'auth/register', register)
        setResponse(res)
        setRegister({
            fname: '',
            lname: '',
            email: '',
            password: '',
            cpassword: ''
        })
        setActive('login')
    }

    let navigate = useNavigate()
    const loginSubmit = async (e) => {
        e.preventDefault()
        let res = await api('POST', 'auth/login', login)
        setResponse(res)
        setLogin({
            email: '',
            password: ''
        })

        // Handle user session & JWT & Redirection
        if(res.type === 'success'){
            setJwtToken(res.authToken)
            setRefreshToken(res.refreshToken)
            setTimeout(() => {
                return navigate("/")
            }, 3000)
        }
    }
    const resetpass = async (e) => {
        e.preventDefault()
        let res = await api('POST', 'auth/reqreset', reset)
        if(res.type==='success'){
            setActive('otp')
            setResponse({message: '', type: ''})
        } else {
            setResponse(res)
        }
    }
    const otp = async (e) => {
        e.preventDefault()
        let res = await api('POST', 'auth/otp', reset)
        if(res.type==='success'){
            setActive('resset')
            setResponse({message: '', type: ''})
        } else {
            setResponse(res)
        }
    }
    const resset = async (e) => {
        e.preventDefault()
        let res = await api('POST', 'auth/resset', reset)
        if(res.type==='success'){
            setResponse(res)
            setTimeout(()=>{
                setActive('login')
                setResponse({message: '', type: ''})
            }, 1000)
        } else {
            setResponse(res)
        }
    }
  return (
    <Fragment>
        <div className="authentification">
            <Link to="/">
                <Home className="getbackHome"/>            
            </Link>
          <section className="contact">
            <div className="contact-wrapper">
                <div className="contFormSec">
                    <h2 className="contact-header">Hate Speech Detection</h2>
                    {(response.message!=='')?<p className={(response.type==='success')?"formNotifySucc":"formNotify"}>{response.message}</p>:null}
                    <form action="contact.php" method="POST" className={(active==='register')?"registration-form":"hide-activity"} onSubmit={(e)=>registerSubmit(e)}>
                        <h3>Register</h3>
                        <div className="cont-group">
                            <div className="cont-gr-flex">
                                <div className="contPut">
                                    <div className="user-input-wrp">
                                        <br/>
                                        <input  type="text" className="inputText id-input" name="fname" value={register.fname} onChange={(e)=>{setRegister({ ...register, [e.target.name]: e.target.value })}}/>
                                        <span className="floating-label">First Name <span style={{color: "red"}}>*</span></span>
                                    </div>
                                    <span id="id-err"></span>
                                </div>
                                <div className="contPut">
                                    <div className="user-input-wrp">
                                        <br/>
                                        <input  type="text" className="inputText id-input" name="lname" value={register.lname} onChange={(e)=>{setRegister({ ...register, [e.target.name]: e.target.value })}}/>
                                        <span className="floating-label">Last Name <span style={{color: "red"}}>*</span></span>
                                    </div>
                                    <span id="id-err"></span>
                                </div>
                            </div>
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="text" className="inputText id-input" name="email" value={register.email} onChange={(e)=>{setRegister({ ...register, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Email address <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="password" className="inputText id-input" name="password" value={register.password} onChange={(e)=>{setRegister({ ...register, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Password <span style={{color: "red"}}>*</span></span>
                            </div>
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="password" className="inputText id-input" name="cpassword" value={register.cpassword} onChange={(e)=>{setRegister({ ...register, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Confirm Password <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <p>have an account? <span onClick={()=>{
                            setActive('login')
                            setResponse({message: '', type: ''})
                        }}>Login here</span></p>
                        <div className="resetting-pass">
                            <input type="submit" value="register" name="contact" className="contact-btn"/>
                        </div>
                    </form>
                    {/* Login To The System */}
                    <form action="contact.php" method="POST" className={(active==='login')?"login-form":"hide-activity"}  onSubmit={(e)=>loginSubmit(e)}>
                        <h3>Login</h3>
                        <div className="cont-group">
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="text" className="inputText id-input" name="email" value={login.email} onChange={(e)=>{setLogin({ ...login, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Email Address <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="password" className="inputText id-input" name="password" value={login.password} onChange={(e)=>{setLogin({ ...login, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Password <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <p>don't have an account? <span onClick={()=>{
                            setActive('register')
                            setResponse({message: '', type: ''})
                        }}>Register here</span></p>
                        <div className="resetting-pass">
                            <input type="submit" value="login" name="contact" className="contact-btn"/>
                            <p><span onClick={()=>{
                                setActive('reset')
                                setResponse({message: '', type: ''})
                            }}>forgot password?</span></p>
                        </div>
                    </form>
                    {/* Reset Password */}
                    <form action="contact.php" method="POST" className={(active==='reset')?"login-form":"hide-activity"}  onSubmit={(e)=>resetpass(e)}>
                        <h3>Request reset OTP</h3>
                        <div className="cont-group">
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="text" className="inputText id-input" name="email" value={reset.email} onChange={(e)=>{setReset({ ...reset, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Email Address <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <div className="resetting-pass">
                            <input type="submit" value="request" name="contact" className="contact-btn"/>
                            <p><span onClick={()=>{
                                setActive('login')
                                setResponse({message: '', type: ''})
                            }}>login</span></p>
                        </div>
                    </form>
                    {/* Reset Password */}
                    <form action="contact.php" method="POST" className={(active==='otp')?"login-form":"hide-activity"}  onSubmit={(e)=>otp(e)}>
                        <h3>Confirm OTP</h3>
                        <div className="cont-group">
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="text" className="inputText id-input" name="otp" value={reset.otp} onChange={(e)=>{setReset({ ...reset, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">OTP <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <div className="resetting-pass">
                            <input type="submit" value="request" name="contact" className="contact-btn"/>
                            <p><span onClick={()=>{
                                setActive('login')
                                setResponse({message: '', type: ''})
                            }}>login</span></p>
                        </div>
                    </form>
                    {/* Reset Password */}
                    <form action="contact.php" method="POST" className={(active==='resset')?"login-form":"hide-activity"}  onSubmit={(e)=>resset(e)}>
                        <h3>Enter New Password</h3>
                        <div className="cont-group">
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="password" className="inputText id-input" name="password" value={reset.password} onChange={(e)=>{setReset({ ...reset, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Password <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                            <div className="user-input-wrp">
                                <br/>
                                <input  type="password" className="inputText id-input" name="cpassword" value={reset.cpassword} onChange={(e)=>{setReset({ ...reset, [e.target.name]: e.target.value })}}/>
                                <span className="floating-label">Confirm Password <span style={{color: "red"}}>*</span></span>
                            </div>
                            <span id="id-err"></span>
                        </div>
                        <div className="resetting-pass">
                            <input type="submit" value="reset" name="contact" className="contact-btn"/>
                            <p><span onClick={()=>{
                                setActive('login')
                                setResponse({message: '', type: ''})
                            }}>login</span></p>
                        </div>
                    </form>
                </div>
            </div>
          </section>
        </div>
    </Fragment>
  )
}

export default Auth