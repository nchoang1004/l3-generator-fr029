---
generated: true
non_normative: true
snapshot_id: "snap:96f8c4c9bb1fbd6f13ba0f2b1a22b3c98fb3e718c6744a39e04ab68535bb4a3f"
owner_component_id: "cmp_bfc26ab6cf618b4444fbaa84f29ba0f77c1a5fdff6b9c679cf9218caa28e7516"
schema_version: "0.1.0"
renderer_version: "slice-render-v2"
template_version: "slice-template-v1"
fact_ids: ["fact:38feeffcb0cf6c5ddf1d3cbaad882692413b2abf1c39c4e96c68eeefb4580378", "fact:442ab82adbd1d4490249ec1092e3cc0c88af2b72ee5fecff0f729a4ff0363194", "fact:44de75a521fe0c25842355f8575018f4d2630b9efe65f419d3b936bb71ff6703", "fact:635e3e9b2e791a0b950ce5af33b71cc1af5eaa14c389a115ee792ebda7226d51", "fact:ec85316077d1ae8e30dd04f6f1f1be88d768a0c52d27a00aaa0ec205a052a60d"]
evidence_ids: ["ev:004d8d8bc5c94384c2d32dc7fc656153f1faaddb672ba4037fa3fbd2097e745b", "ev:0520ab2f0c78ef30d1c60e9f7d6fb9e4eb2e4f4aa3a4a5b242b2c6296bf127d6", "ev:06120c62a399c7cd26f864e1819aee0c6426c63b2185f4836a31b66d54bdb82f", "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98", "ev:07b4749cd8fe2f82dafcd34d2510f121c2be213fa7495db2e6dcc3c37e3686ea", "ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb", "ev:120081f690dad0cbf2ba0b10639c7a4f0ec465d6c56ee6577a5ada9cfbd368e3", "ev:144dfc53edf3281201e8cffea0bd3384229b436fb1ed9915b65c0908b119dc7c", "ev:19114c2871fe44b3e796ff55cde8d0daefa04c26a4af55d41dd4186d8836b964", "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141", "ev:2c2de2f2bed9c97a2eb5d829a0224773b3afc79f36b65ce55912104b40e7e3c1", "ev:2ced91488a01468dd5428a27d437893eedeb024f6f53f860a9e54cf87679e32f", "ev:31e48b2a2fc3bf54ff1cd1a5d8084389d7563587ce2ac714b20b4ff923cd75a0", "ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1", "ev:3ad24e22279fb42a11a8053efcc82687c2e7d64e05168598794ac92845e17a3c", "ev:446f775ec27f4bf269dcd17f8a6ef8bb87e466d660b6b6d5f49f0bd0fe9d38a7", "ev:5c1a20b2838fe5a79396fd7125a62be166fe268ffe271103224e5aa6130bd1ab", "ev:6735edc98807e55c68a10d3fa39221cd3e964f243744142601aaf15988e1daee", "ev:68c0e04c0cbdbafe392e7512db7d31eefb6c45f16e86f2594ef3e26dba4d2aee", "ev:8481e190925055495d76c9c4d10a8244f91dad38c6762add165b0fe90e603193", "ev:876df19272aca0a968874cf1f61d0f3a71f432853894ba12fde7701a7151d722", "ev:88c56e091b4281ab11684a86275bed0cc35214988b46eb226a2c4aa9a0021593", "ev:92da96f9bfa4d149c667e3ac549f405c28e7d4792cc51730c611274c07943f17", "ev:951f34d14e0b2b2ebd00e0dbea91239491b912594706037a55d2715dfdb3716d", "ev:967d1d3c651a9ab6ece7d89d4d5d6897484f70c864bcf85da81ba1f289596263", "ev:98ba26ad2ad75a21218ac9de952e96f34db3582b47e0e599138bbae4a8353fc8", "ev:a2c2abaa95ef18deb17d2a26764f7f6b633b9bcf931182c60cef01e7c14a1ea7", "ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7", "ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc", "ev:b5441029363028e32485ef570a0272a77fe34e6030ce5e7b14aaa5e2a2c8609a", "ev:bf5bdc49cf814c039df6e95d971ecb8fcddd027bec812f2cef0a0763c06e622e", "ev:ca959d6b1b35481644311cf67aa489acbc5dfc2fcb5a9e17dc8a54baa273c74e", "ev:d917c5cdcf6ae888f4fd5a2619340da0ace352d680c98679a6f228c2f3de1c74", "ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39", "ev:ea8b6b2730fb13bac950cd8ac41f094059bd2966afb18561774cd89f5ada748e", "ev:f26acf84c25c69b9efea06428f447110b8a7292180a7d8a915b98fd3b29edaf4"]
---
# API — Public API router

Bản sinh tự động từ phân tích tĩnh, chưa được chủ repository duyệt.

## Endpoint

Bảng cho người đọc. Cột Mã là 8 ký tự đầu của fact ID; mục Truy vết bên dưới có ID đầy đủ và bằng chứng.

| Method | Path | Tham số | Request | Response | Status | Auth | Nhãn | Mã |
|---|---|---|---|---|---|---|---|---|
| POST | /api/v1/auth/refresh | (không có) | RefreshTokenRequest | RefreshTokenResponse | 200 (suy theo fastapi-status-default-v1) | unknown — Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực | inferred / partial | `f:44de75a5` |
| POST | /api/v1/auth/verify | (không có) | VerifyTokenRequest | (không có) | 200 (suy theo fastapi-status-default-v1) | unknown — Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực | inferred / partial | `f:635e3e9b` |
| GET | /api/v1/user | limit (query, integer, tùy chọn); prev (query, integer, tùy chọn) | (không có) | unknown — Response model không phải Pydantic model trong repo: list[GetUserListResponseDTO] | 200 (suy theo fastapi-status-default-v1) | unknown — Có dependency PermissionDependency([IsAdmin]), Provide[Container.user_service]; không kết luận cơ chế xác thực | inferred / partial | `f:ec853160` |
| POST | /api/v1/user | (không có) | CreateUserRequest | CreateUserResponseDTO | 200 (suy theo fastapi-status-default-v1) | unknown — Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực | inferred / partial | `f:38feeffc` |
| POST | /api/v1/user/login | (không có) | LoginRequest | LoginResponse | 200 (suy theo fastapi-status-default-v1) | unknown — Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực | inferred / partial | `f:442ab82a` |


## Model

### CreateUserRequest (request)

Fact `f:fc281e5e` · exact / full · khai ở app/user/adapter/input/api/v1/request/__init__.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| email | string | True | False |
| password1 | string | True | False |
| password2 | string | True | False |
| nickname | string | True | False |
| lat | number | True | False |
| lng | number | True | False |

### CreateUserResponseDTO (response)

Fact `f:1a1953d6` · exact / full · khai ở app/user/application/dto/__init__.py:17

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| email | string | True | False |
| nickname | string | True | False |

### LoginRequest (request)

Fact `f:99434a20` · exact / full · khai ở app/user/adapter/input/api/v1/request/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| email | string | True | False |
| password | string | True | False |

### LoginResponse (response)

Fact `f:13fbdb16` · exact / full · khai ở app/user/adapter/input/api/v1/response/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| token | string | True | False |
| refresh_token | string | True | False |

### RefreshTokenRequest (request)

Fact `f:bdda91a8` · exact / full · khai ở app/auth/adapter/input/api/v1/request/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| token | string | True | False |
| refresh_token | string | True | False |

### RefreshTokenResponse (response)

Fact `f:cded9170` · exact / full · khai ở app/auth/adapter/input/api/v1/response/__init__.py:4

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| token | string | True | False |
| refresh_token | string | True | False |

### VerifyTokenRequest (request)

Fact `f:d737b707` · exact / full · khai ở app/auth/adapter/input/api/v1/request/__init__.py:9

| Field | Kiểu | Bắt buộc | Nullable |
|---|---|---|---|
| token | string | True | False |

## Truy vết

| Application | Method | Path | Handler | Request | Response | Status | Auth | Fact | Evidence | Confidence | Completeness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| app:app/server.py::create_app.app_ | POST | /api/v1/auth/refresh | app.auth.adapter.input.api.v1.auth.refresh_token | fact:bdda91a800e4704eca8f3229d9081cc43270dfa4f212f64da6d7eccfe771eb85 | fact:cded917059d67b5cbe026d3621ecf9da62763176cd4531228f9e305a75c3ae3d | 200 | unknown — Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực | `fact:44de75a521fe0c25842355f8575018f4d2630b9efe65f419d3b936bb71ff6703` | `ev:5c1a20b2838fe5a79396fd7125a62be166fe268ffe271103224e5aa6130bd1ab` (app/auth/adapter/input/api/__init__.py:5), `ev:446f775ec27f4bf269dcd17f8a6ef8bb87e466d660b6b6d5f49f0bd0fe9d38a7` (app/auth/adapter/input/api/__init__.py:6), `ev:a2c2abaa95ef18deb17d2a26764f7f6b633b9bcf931182c60cef01e7c14a1ea7` (app/auth/adapter/input/api/__init__.py:6), `ev:31e48b2a2fc3bf54ff1cd1a5d8084389d7563587ce2ac714b20b4ff923cd75a0` (app/auth/adapter/input/api/v1/auth.py:12), `ev:2c2de2f2bed9c97a2eb5d829a0224773b3afc79f36b65ce55912104b40e7e3c1` (app/auth/adapter/input/api/v1/auth.py:15-20), `ev:92da96f9bfa4d149c667e3ac549f405c28e7d4792cc51730c611274c07943f17` (app/auth/adapter/input/api/v1/auth.py:15), `ev:004d8d8bc5c94384c2d32dc7fc656153f1faaddb672ba4037fa3fbd2097e745b` (app/auth/adapter/input/api/v1/auth.py:16), `ev:d917c5cdcf6ae888f4fd5a2619340da0ace352d680c98679a6f228c2f3de1c74` (app/auth/adapter/input/api/v1/auth.py:17), `ev:967d1d3c651a9ab6ece7d89d4d5d6897484f70c864bcf85da81ba1f289596263` (app/auth/adapter/input/api/v1/auth.py:21), `ev:06120c62a399c7cd26f864e1819aee0c6426c63b2185f4836a31b66d54bdb82f` (app/server.py:26), `ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98` (app/server.py:77-85), `ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141` (app/server.py:86) | inferred | partial |
| app:app/server.py::create_app.app_ | POST | /api/v1/auth/verify | app.auth.adapter.input.api.v1.auth.verify_token | fact:d737b707c4cd72f04ebcea0d852da2b9168dd8eb578962dedeeda9d56c3226a3 | (rỗng) | 200 | unknown — Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực | `fact:635e3e9b2e791a0b950ce5af33b71cc1af5eaa14c389a115ee792ebda7226d51` | `ev:5c1a20b2838fe5a79396fd7125a62be166fe268ffe271103224e5aa6130bd1ab` (app/auth/adapter/input/api/__init__.py:5), `ev:446f775ec27f4bf269dcd17f8a6ef8bb87e466d660b6b6d5f49f0bd0fe9d38a7` (app/auth/adapter/input/api/__init__.py:6), `ev:a2c2abaa95ef18deb17d2a26764f7f6b633b9bcf931182c60cef01e7c14a1ea7` (app/auth/adapter/input/api/__init__.py:6), `ev:31e48b2a2fc3bf54ff1cd1a5d8084389d7563587ce2ac714b20b4ff923cd75a0` (app/auth/adapter/input/api/v1/auth.py:12), `ev:144dfc53edf3281201e8cffea0bd3384229b436fb1ed9915b65c0908b119dc7c` (app/auth/adapter/input/api/v1/auth.py:30), `ev:b5441029363028e32485ef570a0272a77fe34e6030ce5e7b14aaa5e2a2c8609a` (app/auth/adapter/input/api/v1/auth.py:30), `ev:ea8b6b2730fb13bac950cd8ac41f094059bd2966afb18561774cd89f5ada748e` (app/auth/adapter/input/api/v1/auth.py:30-32), `ev:120081f690dad0cbf2ba0b10639c7a4f0ec465d6c56ee6577a5ada9cfbd368e3` (app/auth/adapter/input/api/v1/auth.py:33), `ev:06120c62a399c7cd26f864e1819aee0c6426c63b2185f4836a31b66d54bdb82f` (app/server.py:26), `ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98` (app/server.py:77-85), `ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141` (app/server.py:86) | inferred | partial |
| app:app/server.py::create_app.app_ | GET | /api/v1/user | app.user.adapter.input.api.v1.user.get_user_list | (rỗng) | unknown — Response model không phải Pydantic model trong repo: list[GetUserListResponseDTO] | 200 | unknown — Có dependency PermissionDependency([IsAdmin]), Provide[Container.user_service]; không kết luận cơ chế xác thực | `fact:ec85316077d1ae8e30dd04f6f1f1be88d768a0c52d27a00aaa0ec205a052a60d` | `ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39` (app/server.py:25), `ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98` (app/server.py:77-85), `ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141` (app/server.py:86), `ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1` (app/user/adapter/input/api/__init__.py:5), `ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7` (app/user/adapter/input/api/__init__.py:6), `ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc` (app/user/adapter/input/api/__init__.py:6), `ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb` (app/user/adapter/input/api/v1/user.py:12), `ev:6735edc98807e55c68a10d3fa39221cd3e964f243744142601aaf15988e1daee` (app/user/adapter/input/api/v1/user.py:15), `ev:8481e190925055495d76c9c4d10a8244f91dad38c6762add165b0fe90e603193` (app/user/adapter/input/api/v1/user.py:15-21), `ev:3ad24e22279fb42a11a8053efcc82687c2e7d64e05168598794ac92845e17a3c` (app/user/adapter/input/api/v1/user.py:16), `ev:bf5bdc49cf814c039df6e95d971ecb8fcddd027bec812f2cef0a0763c06e622e` (app/user/adapter/input/api/v1/user.py:22), `ev:951f34d14e0b2b2ebd00e0dbea91239491b912594706037a55d2715dfdb3716d` (app/user/adapter/input/api/v1/user.py:23) | inferred | partial |
| app:app/server.py::create_app.app_ | POST | /api/v1/user | app.user.adapter.input.api.v1.user.create_user | fact:fc281e5e8986c99d9c30665f71a7d59cce93ed31e9517476bd89d6af59de31ba | fact:1a1953d67d3fe8669cb674f3ff9d24839b8ab5561a2229e56227987bfb0f6707 | 200 | unknown — Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực | `fact:38feeffcb0cf6c5ddf1d3cbaad882692413b2abf1c39c4e96c68eeefb4580378` | `ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39` (app/server.py:25), `ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98` (app/server.py:77-85), `ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141` (app/server.py:86), `ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1` (app/user/adapter/input/api/__init__.py:5), `ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7` (app/user/adapter/input/api/__init__.py:6), `ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc` (app/user/adapter/input/api/__init__.py:6), `ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb` (app/user/adapter/input/api/v1/user.py:12), `ev:07b4749cd8fe2f82dafcd34d2510f121c2be213fa7495db2e6dcc3c37e3686ea` (app/user/adapter/input/api/v1/user.py:29), `ev:68c0e04c0cbdbafe392e7512db7d31eefb6c45f16e86f2594ef3e26dba4d2aee` (app/user/adapter/input/api/v1/user.py:29-34), `ev:98ba26ad2ad75a21218ac9de952e96f34db3582b47e0e599138bbae4a8353fc8` (app/user/adapter/input/api/v1/user.py:30), `ev:0520ab2f0c78ef30d1c60e9f7d6fb9e4eb2e4f4aa3a4a5b242b2c6296bf127d6` (app/user/adapter/input/api/v1/user.py:31), `ev:ca959d6b1b35481644311cf67aa489acbc5dfc2fcb5a9e17dc8a54baa273c74e` (app/user/adapter/input/api/v1/user.py:35) | inferred | partial |
| app:app/server.py::create_app.app_ | POST | /api/v1/user/login | app.user.adapter.input.api.v1.user.login | fact:99434a208ea6c2c663f136451a63770811ed1885de9d06ee354e1be7248fa981 | fact:13fbdb16798730e1d0ef943e7e1d78bdcc7680abd21649e08bdc38d8837b2316 | 200 | unknown — Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực | `fact:442ab82adbd1d4490249ec1092e3cc0c88af2b72ee5fecff0f729a4ff0363194` | `ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39` (app/server.py:25), `ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98` (app/server.py:77-85), `ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141` (app/server.py:86), `ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1` (app/user/adapter/input/api/__init__.py:5), `ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7` (app/user/adapter/input/api/__init__.py:6), `ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc` (app/user/adapter/input/api/__init__.py:6), `ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb` (app/user/adapter/input/api/v1/user.py:12), `ev:876df19272aca0a968874cf1f61d0f3a71f432853894ba12fde7701a7151d722` (app/user/adapter/input/api/v1/user.py:43-48), `ev:f26acf84c25c69b9efea06428f447110b8a7292180a7d8a915b98fd3b29edaf4` (app/user/adapter/input/api/v1/user.py:43), `ev:88c56e091b4281ab11684a86275bed0cc35214988b46eb226a2c4aa9a0021593` (app/user/adapter/input/api/v1/user.py:44), `ev:2ced91488a01468dd5428a27d437893eedeb024f6f53f860a9e54cf87679e32f` (app/user/adapter/input/api/v1/user.py:45), `ev:19114c2871fe44b3e796ff55cde8d0daefa04c26a4af55d41dd4186d8836b964` (app/user/adapter/input/api/v1/user.py:49) | inferred | partial |

Khối OpenAPI chỉ chứa operation đủ dữ kiện; phần bị bỏ ở `x-analysis.omitted_operations`.

```json
{
  "components": {
    "schemas": {
      "CreateUserRequest_fc281e5e": {
        "properties": {
          "email": {
            "type": "string"
          },
          "lat": {
            "type": "number"
          },
          "lng": {
            "type": "number"
          },
          "nickname": {
            "type": "string"
          },
          "password1": {
            "type": "string"
          },
          "password2": {
            "type": "string"
          }
        },
        "required": [
          "email",
          "lat",
          "lng",
          "nickname",
          "password1",
          "password2"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:fc281e5e8986c99d9c30665f71a7d59cce93ed31e9517476bd89d6af59de31ba"
          ]
        }
      },
      "CreateUserResponseDTO_1a1953d6": {
        "properties": {
          "email": {
            "type": "string"
          },
          "nickname": {
            "type": "string"
          }
        },
        "required": [
          "email",
          "nickname"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:1a1953d67d3fe8669cb674f3ff9d24839b8ab5561a2229e56227987bfb0f6707"
          ]
        }
      },
      "LoginRequest_99434a20": {
        "properties": {
          "email": {
            "type": "string"
          },
          "password": {
            "type": "string"
          }
        },
        "required": [
          "email",
          "password"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:99434a208ea6c2c663f136451a63770811ed1885de9d06ee354e1be7248fa981"
          ]
        }
      },
      "LoginResponse_13fbdb16": {
        "properties": {
          "refresh_token": {
            "type": "string"
          },
          "token": {
            "type": "string"
          }
        },
        "required": [
          "refresh_token",
          "token"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:13fbdb16798730e1d0ef943e7e1d78bdcc7680abd21649e08bdc38d8837b2316"
          ]
        }
      },
      "RefreshTokenRequest_bdda91a8": {
        "properties": {
          "refresh_token": {
            "type": "string"
          },
          "token": {
            "type": "string"
          }
        },
        "required": [
          "refresh_token",
          "token"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:bdda91a800e4704eca8f3229d9081cc43270dfa4f212f64da6d7eccfe771eb85"
          ]
        }
      },
      "RefreshTokenResponse_cded9170": {
        "properties": {
          "refresh_token": {
            "type": "string"
          },
          "token": {
            "type": "string"
          }
        },
        "required": [
          "refresh_token",
          "token"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:cded917059d67b5cbe026d3621ecf9da62763176cd4531228f9e305a75c3ae3d"
          ]
        }
      },
      "VerifyTokenRequest_d737b707": {
        "properties": {
          "token": {
            "type": "string"
          }
        },
        "required": [
          "token"
        ],
        "type": "object",
        "x-analysis": {
          "fact_ids": [
            "fact:d737b707c4cd72f04ebcea0d852da2b9168dd8eb578962dedeeda9d56c3226a3"
          ]
        }
      }
    }
  },
  "info": {
    "title": "Public API router",
    "version": "generated-v1"
  },
  "openapi": "3.1.0",
  "paths": {
    "/api/v1/auth/refresh": {
      "post": {
        "operationId": "op_44de75a521fe0c25",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/RefreshTokenRequest_bdda91a8"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/RefreshTokenResponse_cded9170"
                }
              }
            },
            "description": "Status code suy theo fastapi-status-default-v1"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py::create_app.app_",
          "evidence_ids": [
            "ev:004d8d8bc5c94384c2d32dc7fc656153f1faaddb672ba4037fa3fbd2097e745b",
            "ev:06120c62a399c7cd26f864e1819aee0c6426c63b2185f4836a31b66d54bdb82f",
            "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98",
            "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141",
            "ev:2c2de2f2bed9c97a2eb5d829a0224773b3afc79f36b65ce55912104b40e7e3c1",
            "ev:31e48b2a2fc3bf54ff1cd1a5d8084389d7563587ce2ac714b20b4ff923cd75a0",
            "ev:446f775ec27f4bf269dcd17f8a6ef8bb87e466d660b6b6d5f49f0bd0fe9d38a7",
            "ev:5c1a20b2838fe5a79396fd7125a62be166fe268ffe271103224e5aa6130bd1ab",
            "ev:92da96f9bfa4d149c667e3ac549f405c28e7d4792cc51730c611274c07943f17",
            "ev:967d1d3c651a9ab6ece7d89d4d5d6897484f70c864bcf85da81ba1f289596263",
            "ev:a2c2abaa95ef18deb17d2a26764f7f6b633b9bcf931182c60cef01e7c14a1ea7",
            "ev:d917c5cdcf6ae888f4fd5a2619340da0ace352d680c98679a6f228c2f3de1c74"
          ],
          "fact_ids": [
            "fact:44de75a521fe0c25842355f8575018f4d2630b9efe65f419d3b936bb71ff6703"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/api/v1/auth/verify": {
      "post": {
        "operationId": "op_635e3e9b2e791a0b",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/VerifyTokenRequest_d737b707"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi-status-default-v1; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py::create_app.app_",
          "evidence_ids": [
            "ev:06120c62a399c7cd26f864e1819aee0c6426c63b2185f4836a31b66d54bdb82f",
            "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98",
            "ev:120081f690dad0cbf2ba0b10639c7a4f0ec465d6c56ee6577a5ada9cfbd368e3",
            "ev:144dfc53edf3281201e8cffea0bd3384229b436fb1ed9915b65c0908b119dc7c",
            "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141",
            "ev:31e48b2a2fc3bf54ff1cd1a5d8084389d7563587ce2ac714b20b4ff923cd75a0",
            "ev:446f775ec27f4bf269dcd17f8a6ef8bb87e466d660b6b6d5f49f0bd0fe9d38a7",
            "ev:5c1a20b2838fe5a79396fd7125a62be166fe268ffe271103224e5aa6130bd1ab",
            "ev:a2c2abaa95ef18deb17d2a26764f7f6b633b9bcf931182c60cef01e7c14a1ea7",
            "ev:b5441029363028e32485ef570a0272a77fe34e6030ce5e7b14aaa5e2a2c8609a",
            "ev:ea8b6b2730fb13bac950cd8ac41f094059bd2966afb18561774cd89f5ada748e"
          ],
          "fact_ids": [
            "fact:635e3e9b2e791a0b950ce5af33b71cc1af5eaa14c389a115ee792ebda7226d51"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Có dependency Provide[Container.jwt_service]; không kết luận cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/api/v1/user": {
      "get": {
        "operationId": "op_ec85316077d1ae8e",
        "parameters": [
          {
            "in": "query",
            "name": "limit",
            "required": false,
            "schema": {
              "type": "integer"
            }
          },
          {
            "in": "query",
            "name": "prev",
            "required": false,
            "schema": {
              "type": "integer"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Status code suy theo fastapi-status-default-v1; nội dung response chưa xác định"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py::create_app.app_",
          "evidence_ids": [
            "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98",
            "ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb",
            "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141",
            "ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1",
            "ev:3ad24e22279fb42a11a8053efcc82687c2e7d64e05168598794ac92845e17a3c",
            "ev:6735edc98807e55c68a10d3fa39221cd3e964f243744142601aaf15988e1daee",
            "ev:8481e190925055495d76c9c4d10a8244f91dad38c6762add165b0fe90e603193",
            "ev:951f34d14e0b2b2ebd00e0dbea91239491b912594706037a55d2715dfdb3716d",
            "ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7",
            "ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc",
            "ev:bf5bdc49cf814c039df6e95d971ecb8fcddd027bec812f2cef0a0763c06e622e",
            "ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39"
          ],
          "fact_ids": [
            "fact:ec85316077d1ae8e30dd04f6f1f1be88d768a0c52d27a00aaa0ec205a052a60d"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Có dependency PermissionDependency([IsAdmin]), Provide[Container.user_service]; không kết luận cơ chế xác thực"
            },
            {
              "field": "response_model_ids",
              "reason": "Response model không phải Pydantic model trong repo: list[GetUserListResponseDTO]"
            }
          ]
        }
      },
      "post": {
        "operationId": "op_38feeffcb0cf6c5d",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/CreateUserRequest_fc281e5e"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/CreateUserResponseDTO_1a1953d6"
                }
              }
            },
            "description": "Status code suy theo fastapi-status-default-v1"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py::create_app.app_",
          "evidence_ids": [
            "ev:0520ab2f0c78ef30d1c60e9f7d6fb9e4eb2e4f4aa3a4a5b242b2c6296bf127d6",
            "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98",
            "ev:07b4749cd8fe2f82dafcd34d2510f121c2be213fa7495db2e6dcc3c37e3686ea",
            "ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb",
            "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141",
            "ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1",
            "ev:68c0e04c0cbdbafe392e7512db7d31eefb6c45f16e86f2594ef3e26dba4d2aee",
            "ev:98ba26ad2ad75a21218ac9de952e96f34db3582b47e0e599138bbae4a8353fc8",
            "ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7",
            "ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc",
            "ev:ca959d6b1b35481644311cf67aa489acbc5dfc2fcb5a9e17dc8a54baa273c74e",
            "ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39"
          ],
          "fact_ids": [
            "fact:38feeffcb0cf6c5ddf1d3cbaad882692413b2abf1c39c4e96c68eeefb4580378"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực"
            }
          ]
        }
      }
    },
    "/api/v1/user/login": {
      "post": {
        "operationId": "op_442ab82adbd1d449",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/LoginRequest_99434a20"
              }
            }
          },
          "required": true
        },
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/LoginResponse_13fbdb16"
                }
              }
            },
            "description": "Status code suy theo fastapi-status-default-v1"
          }
        },
        "x-analysis": {
          "application_id": "app:app/server.py::create_app.app_",
          "evidence_ids": [
            "ev:067ce455bcdd884a250b0c14e627c588d2499756891867dd3c01fef18f872e98",
            "ev:1139d4ce39c973e3c08b94668123e454151712509ea725d5a46c2449cd5a2afb",
            "ev:19114c2871fe44b3e796ff55cde8d0daefa04c26a4af55d41dd4186d8836b964",
            "ev:2b53b8148936f7737b9630285c28cb2beb32ec6b2fee5e48fe4caf9a4bff6141",
            "ev:2ced91488a01468dd5428a27d437893eedeb024f6f53f860a9e54cf87679e32f",
            "ev:344cc3d99e6d55a56077484b99bccb9b7f295d84443ae53f4153cc3050bc5df1",
            "ev:876df19272aca0a968874cf1f61d0f3a71f432853894ba12fde7701a7151d722",
            "ev:88c56e091b4281ab11684a86275bed0cc35214988b46eb226a2c4aa9a0021593",
            "ev:b14713759abd8dc60bc70593c9fa7f5c4dffb22e8def79eea0751a21a2cf4fb7",
            "ev:b2abf6180ebac3c2b608c95454c60d840eee19ddd81211478106428efcd5e2bc",
            "ev:e0ab2c87a9428b5cfbf2222c6cb3cf0e5b242f1bb9cfee208300b29c97efdd39",
            "ev:f26acf84c25c69b9efea06428f447110b8a7292180a7d8a915b98fd3b29edaf4"
          ],
          "fact_ids": [
            "fact:442ab82adbd1d4490249ec1092e3cc0c88af2b72ee5fecff0f729a4ff0363194"
          ],
          "unknowns": [
            {
              "field": "auth",
              "reason": "Có dependency Provide[Container.user_service]; không kết luận cơ chế xác thực"
            }
          ]
        }
      }
    }
  },
  "x-analysis": {
    "omitted_operations": []
  }
}
```
