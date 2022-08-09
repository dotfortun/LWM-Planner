const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      user_token: null,
      user: {},
      pilots: [],
      missions: [],
      shop: {
        frame: [],
        weapon: [],
        system: [],
        mod: [],
      },
    },
    actions: {
      getAuthOptions: (method = "GET", body = {}) => {
        if (method === "GET") {
          return {
            method: method,
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${getStore().user_token}`,
            },
          };
        } else {
          return {
            method: method,
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${getStore().user_token}`,
            },
            body: JSON.stringify(body),
          };
        }
      },

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

      getActiveUser: () => {
        const opts = getActions().getAuthOptions("GET");
        return fetch(process.env.BACKEND_URL + "/api/users/active", opts)
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((data) => setStore({ user: data }))
          .then(() => getActions().dehydrate());
      },

      updateActiveUser: (body) => {
        const opts = getActions().getAuthOptions("PUT");
        return fetch(process.env.BACKEND_URL + "/api/users/active", opts)
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((data) => console.log(data))
          .then(() => getActions().dehydrate());
      },

      getActivePilots: () => {
        const opts = getActions().getAuthOptions("GET");
        return fetch(process.env.BACKEND_URL + "/api/users/pilots", opts)
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((resp) => {
            console.log(resp);
            return resp;
          })
          .then((data) => setStore({ pilots: data?.pilots }))
          .then(() => getActions().dehydrate())
          .catch((err) => console.log(err));
      },

      getShop: () => {
        const opts = getActions().getAuthOptions("GET");
        return fetch(process.env.BACKEND_URL + "/api/shop", opts)
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((data) => {
            console.log(data);
            return data;
          })
          .then((data) => setStore({ shop: data?.shop_items }))
          .then(() => getActions().dehydrate());
      },

      getMissions: (page = 1, per_page = 20) => {
        const params = new URLSearchParams({
          page: page,
          per_page: per_page,
        });
        const opts = getActions().getAuthOptions("GET");
        return fetch(
          [process.env.BACKEND_URL, "/api/missions", "/?" + params].join(""),
          opts
        )
          .then((resp) => {
            if (!resp.ok) {
              throw Error("Invalid login");
            }
            return resp;
          })
          .then((resp) => resp.json())
          .then((data) => setStore({ missions: data.missions }))
          .then(() => getActions().dehydrate());
      },

      dehydrate: () => {
        for (const key in getStore()) {
          sessionStorage.setItem(key, JSON.stringify(getStore()[key]));
        }
      },

      rehydrate: () => {
        for (const key in getStore()) {
          let update = {};
          update[key] = JSON.parse(sessionStorage.getItem(key));
          setStore(update);
        }
        return new Promise((resp) => resp);
      },
    },
  };
};

export default getState;
