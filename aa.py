import dns.resolver

answer = dns.resolver.resolve('youtube.com', 'A')
for server in answer:
    print(server.to_txt())
