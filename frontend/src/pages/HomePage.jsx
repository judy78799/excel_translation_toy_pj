import styled from 'styled-components';
import { Link } from 'react-router-dom';

const HomeContainer = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-md);
`;

const HeroSection = styled.div`
  text-align: center;
  max-width: 800px;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: var(--space-md);
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: fadeIn var(--transition-slow);
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: var(--space-xl);
  line-height: 1.8;
  animation: slideIn var(--transition-slow) 0.2s;
`;

const Features = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-md);
  margin: var(--space-xl) 0;
`;

const Feature = styled.div`
  padding: var(--space-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  transition: all var(--transition-normal);
  
  &:hover {
    transform: translateY(-4px);
    border-color: var(--primary);
    box-shadow: var(--shadow-glow);
  }
  
  .icon {
    font-size: 2rem;
    margin-bottom: var(--space-sm);
  }
  
  h3 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.1rem;
  }
`;

const CTAButton = styled(Link)`
  display: inline-block;
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  text-decoration: none;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
  margin-top: var(--space-lg);
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
  }
`;

export const HomePage = () => {
    return (
        <HomeContainer>
            <HeroSection>
                <Title>Excel Translation Service</Title>
                <Subtitle>
                    Upload your Excel files and translate content instantly with our powerful translation engine
                </Subtitle>

                <Features>
                    <Feature>
                        <div className="icon">⚡</div>
                        <h3>Fast Processing</h3>
                    </Feature>
                    <Feature>
                        <div className="icon">🌍</div>
                        <h3>Multi-language</h3>
                    </Feature>
                    <Feature>
                        <div className="icon">📊</div>
                        <h3>Excel Support</h3>
                    </Feature>
                    <Feature>
                        <div className="icon">🔒</div>
                        <h3>Secure</h3>
                    </Feature>
                </Features>

                <CTAButton to="/translate">Start Translating →</CTAButton>
            </HeroSection>
        </HomeContainer>
    );
};
