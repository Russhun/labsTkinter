import secrets
print(secrets.token_hex(8))

# async def check_ping(self):
#     while self._ping_flag:
#         start = time.time_ns()
#         await self.session.get("http://127.0.0.1:8000/ping")
#         s_ping = f"ping: {int((time.time_ns()-start)/10**6)}ms"
#         self.menu_canvas.ping_label.configure(text=s_ping)
#         await asyncio.sleep(2)