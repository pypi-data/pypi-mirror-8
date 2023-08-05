
      subroutine pair(i)

      include "common.f90"

!+-------------------+
!| Get thread number |
!+-------------------+
      icpu=1
!$    icpu=OMP_GET_THREAD_NUM()+1

!+-----------------------------------------------+
!| Loop over neighbours j to compute pair energy |
!+-----------------------------------------------+
      do jj=1,num(i)
      if (dr(i,jj).lt.a1+a2*z(i)-0.001) then
        rij=dr(i,jj)
        arg=1.0/(rij-a1-a2*z(i))
        bond=exp(-beta*z(i)*z(i))
        r4=1.0/rij**4
        r5=r4/rij

        part1=bb*r4 - bond
        part2=aa*exp(sigma*arg)
        u2i(icpu)=u2i(icpu) + part1*part2
        f22= part2*(2.0*beta*z(i)*bond + part1*sigma*arg*arg*a2)

!+-------------------------------+
!| Forces due to neighbours of i |
!+-------------------------------+
        do kk=1,num(i)
        if ((jj.eq.kk).or.(finiteforce(kk))) then
          k=near(i,kk)
          do ind=1,3
            dxr= kron(jj,kk) * dxdr(i,kk,ind)

            part3= -4.0*bb*r5*dxr + 2.0*beta*z(i)*bond*dzdx(kk,ind)
            part4= -sigma*arg*arg * (dxr - a2*dzdx(kk,ind))
            f2= part2*(part3 + part1*part4)

            fxx(i,ind,icpu) = fxx(i,ind,icpu) - f2
            fxx(k,ind,icpu) = fxx(k,ind,icpu) + f2
            !if (calcstress) call stress(i,kk,f2,ind)
          end do

!+---------------------------------------------+
!| Forces due to neighbours-of-neighbours of i |
!+---------------------------------------------+
          do mm=1,num(k)
          if (finiteforce2(kk,mm)) then
            m=near(k,mm)
            do ind=1,3
              f2= f22*dzdxx(kk,mm,ind)
              fxx(k,ind,icpu) = fxx(k,ind,icpu) - f2
              fxx(m,ind,icpu) = fxx(m,ind,icpu) + f2
              !if (calcstress) call stress(k,mm,f2,ind)
            end do
          end if
          end do

        end if
        end do
      end if
      end do

      end

