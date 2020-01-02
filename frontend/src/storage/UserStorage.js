class UserStorage 
{
    constructor() {
        this.data = {
            pk: null,
            username: null,
            email: null,
            display_group: null,
            is_active: null,
            is_staff: null,
            date_joined: null
        }

    }
    
    setData(data) {
        this.data = data
    }

    getData() {
        return this.data
    }

    setLocalStorageData() {
        localStorage.setItem('user', this.data)
    }
    
    getLocalStorageData() {
        localStorage.getItem('user')
    }

    setUsername(username) {
        this.data.username = username
    }
    
    getUsername() {
        return this.data.username
    }

    setEmail(email) {
        this.data.email = email
    }

    getEmail() {
        return this.data.email
    }
    
    setDisplayGroup(display_group) {
        this.data.display_group = display_group
    }

    getDisplayGroup() {
        return this.
    }
}

export default UserStorage