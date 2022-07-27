const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      user_token: null,
    },
    actions: {
      login: (email, pass) => {
        const opts = {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: pass,
          }),
        };
        return fetch(process.env.BACKEND_URL + "/api/login", opts)
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((data) => setStore({ user_token: data?.token }))
          .then(() => getActions().dehydrate());
      },
      dehydrate: () => {
        for (const key in getStore()) {
          sessionStorage.setItem(key, getStore()[key]);
        }
      },
      rehydrate: () => {
        for (const key in getStore()) {
          let update = {};
          update[key] = sessionStorage.getItem(key);
          setStore(update);
        }
      },
    },
  };
};

export default getState;
