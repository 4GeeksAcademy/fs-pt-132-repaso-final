import { useState } from "react"

const New_Post = () => {

    const [title, setTitle] = useState()

    const handleSubmit = async e => {
        e.preventDefault();
        try {
            const resp = await fetch(import.meta.env.VITE_BACKEND_URL + "api/post", {
                method: "POST",
                headers: {
                    "Content-Type": 'application/json',
                    "Authorization": "Bearer " + localStorage.getItem('token') // permite acceder a @jwt_required
                },
                body: JSON.stringify({title:title})
            });
            if (!resp.ok) throw new Error('error!')
            const data = await resp.json();

        } catch (error) {
            console.log(error)
        }

    }


return (
    <form onSubmit={handleSubmit}>

        <input type="text" onChange={e=>setTitle(e.target.value)}/>
        <input type="submit" />

    </form>
)

}

export default New_Post