import { useState } from "react"
import useGlobalReducer from "../hooks/useGlobalReducer";
import { useNavigate } from "react-router-dom";

const Auth = () => {
    const {dispatch} = useGlobalReducer();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        type: 'login'
    });



    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const resp = await fetch(import.meta.env.VITE_BACKEND_URL + "api/" + formData.type, {
                method: "POST",
                headers: {
                    "Content-Type": 'application/json'
                },
                body: JSON.stringify(formData)
            });
            if (!resp.ok) throw new Error('error!')
            const data = await resp.json();

            dispatch({
                type: "login",
                payload: {
                    user: data.user
                }
            })
            localStorage.setItem('token', data.token)
            navigate('/private')
        } catch (error) {
            console.log(error)
        }



    }

    const handleType = () => setFormData({ ...formData, ['type']: formData.type === 'login' ? "register" : "login" })



    return (
        <div>
            <button onClick={handleType}>change to {formData.type === 'login' ? "login" : "register"}</button>
            <form onSubmit={handleSubmit}>
                <input name="email" value={formData.email} onChange={handleChange} type="email" />
                <input name="password" value={formData.password} onChange={handleChange} type="password" />
                <input type="submit" />

            </form>
        </div>
    )

}


export default Auth